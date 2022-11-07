import ctypes  # You see a ctypes import, you know this is going to be good
import dis
import sys
import types
import threading
import traceback

# Problems which can be solved with more work if you're mad:
# - No block stack support, so no resuming from within a try / except block, with blocks, or async for block.
# - Nested functions (__closure__) and coroutines not supported
# - EXTENDED_ARG not supported, so jumps within code objects must always be fewer than 256 bytes.

MAGIC = 0xdd

# The most recent error, retrievable with err(). Use TLS for this because I'm not a monster.
_last_error = threading.local()
_last_error.err = None

ABS_JUMPS = set(dis.hasjabs)

for _name, _opcode in dis.opmap.items():
    globals()[_name] = _opcode

class DepthNotFound(Exception):
    pass

def _get_value_stack_depth(co_code, target_idx):
    " Find the value stack depth after having executed up to (and including) the instruction at target_idx."
    class Found(Exception):
        def __init__(self, depth):
            self.depth = depth

    seen_pc = set()

    def _interpret(pc, depth):
        found = False
        while not found:
            found = pc == target_idx

            instr = co_code[pc]
            arg = co_code[pc + 1]
            pc += 2

            if pc in seen_pc:
                return

            seen_pc.add(pc)
            if instr in {POP_TOP, INPLACE_POWER, INPLACE_MULTIPLY, INPLACE_MATRIX_MULTIPLY, INPLACE_TRUE_DIVIDE,
                         INPLACE_MODULO, INPLACE_ADD, INPLACE_SUBTRACT, INPLACE_LSHIFT, INPLACE_RSHIFT, INPLACE_AND,
                         INPLACE_XOR, INPLACE_OR, PRINT_EXPR, SET_ADD, LIST_APPEND, YIELD_VALUE, YIELD_FROM,
                         IMPORT_STAR, STORE_NAME, DELETE_ATTR, STORE_GLOBAL, LIST_EXTEND, SET_UPDATE, DICT_UPDATE,
                         DICT_MERGE, COMPARE_OP, IS_OP, CONTAINS_OP, IMPORT_NAME, STORE_FAST, STORE_DEREF,
                         BINARY_POWER, BINARY_MULTIPLY, BINARY_MATRIX_MULTIPLY, BINARY_FLOOR_DIVIDE,
                         BINARY_TRUE_DIVIDE, BINARY_MODULO, BINARY_ADD, BINARY_SUBTRACT,
                         BINARY_SUBSCR, BINARY_LSHIFT, BINARY_RSHIFT, BINARY_AND, BINARY_XOR, BINARY_OR}:
                depth -= 1
            elif instr in {POP_JUMP_IF_TRUE, POP_JUMP_IF_FALSE}:
                depth -= 1
                _interpret(arg, depth)
            elif instr in {JUMP_IF_TRUE_OR_POP, JUMP_IF_FALSE_OR_POP}:
                _interpret(arg, depth)
                depth -= 1
            elif instr in {DELETE_SUBSCR, MAP_ADD, BUILD_SLICE, STORE_ATTR}:
                depth -= 2
            elif instr in {JUMP_IF_NOT_EXC_MATCH}:
                depth -= 2
                _interpret(pc + arg, depth)
            elif instr in {STORE_SUBSCR}:
                depth -= 3
            elif instr == RAISE_VARARGS:
                depth -= arg
            elif instr == CALL_FUNCTION:
                # pop arg parameters, pop function object, push result.
                depth -= arg
            elif instr == CALL_FUNCTION_KW:
                # pop kw tuple, pop arg kw, pop function object, push result.
                depth -= (arg + 1)
            elif instr == CALL_FUNCTION_EX:
                # pop args, pop function object, maybe pop kw dict, push result.
                depth -= 1
                if arg & 1:
                    depth -= 1
            elif instr == CALL_METHOD:
                # pop args, pop object, pop method, push result
                depth -= (arg + 1)
            elif instr in (BUILD_TUPLE, BUILD_LIST, BUILD_SET, BUILD_STRING):
                depth -= (arg - 1)  # a new object is pushed
            elif instr in {DUP_TOP, GET_ANEXT, BEFORE_ASYNC_WITH, LOAD_BUILD_CLASS, LOAD_CONST, LOAD_NAME, IMPORT_FROM,
                           LOAD_GLOBAL, LOAD_FAST, LOAD_CLOSURE, LOAD_DEREF, LOAD_CLASSDEREF, LOAD_METHOD}:
                depth += 1
            elif instr in {DUP_TOP_TWO, SETUP_WITH}:
                depth += 2
            elif instr == UNPACK_SEQUENCE:
                depth += (arg - 1)  # TOS is popped
            elif instr == UNPACK_EX:
                depth += arg
            elif instr == BUILD_MAP:
                depth += ((2 * arg) + 1)  # a new object is pushed
            elif instr == BUILD_CONST_KEY_MAP:
                depth += (arg + 1 + 1)
            elif instr == FOR_ITER:
                _interpret(pc + arg, depth - 1)
                depth += 1
            elif instr == MAKE_FUNCTION:
                depth -= 2  # function code and name
                while arg:
                    depth += 1
                    arg >>= 1
                depth += 1  # the new function
            elif instr == FORMAT_VALUE:
                if arg & 0x4 == 0x4:
                    depth -= 1
            elif instr == JUMP_ABSOLUTE:
                pc = arg
            elif instr == EXTENDED_ARG:
                raise NotImplementedError()
            elif instr == RETURN_VALUE:
                return

            #print(f'{pc}\t{dis.opname[instr]}\t{arg}\t{depth}')

            if found:
                raise Found(depth)

    try:
        _interpret(0, 0)
    except Found as e:
        return e.depth

    raise DepthNotFound(target_idx)

class Frame(ctypes.Structure):
    pass

# source: Python3.9/Include/cpython/frameobject.h
# There are more members after f_valuestack which are omitted here.
Frame._fields_ = [
    ("ob_refcnt", ctypes.c_ssize_t),
    ("ob_type", ctypes.c_void_p),
    ("ob_size", ctypes.c_ssize_t),
    ("f_back", ctypes.POINTER(Frame)),
    ("f_code", ctypes.py_object),
    ("f_builtins", ctypes.py_object),
    ("f_globals", ctypes.py_object),
    ("f_locals", ctypes.py_object),
    ("f_valuestack", ctypes.POINTER(ctypes.py_object))]

class ObliteratedByException:
    def __repr__(self):
        return '<ObliteratedByException>'

def _fetch_value_stack(c_frame, count):
    """
    Return 'count' values from the value stack of 'frame'. Implementation- and version-specific (CPython 3.9).
    """
    if count <= 0:
        return []

    frame = Frame.from_address(id(c_frame))

    values = []
    for i in range(count):
        try:
            values.append(frame.f_valuestack[i])
        except ValueError:
            # Very likely "PyObject is NULL". This happens because CPython uses a NULL return value to signal
            # an exception. If an operation triggered by an opcode causes an exception, that operation's "result"
            # of NULL will be written to the stack before the exception machinery is started.
            values.append(ObliteratedByException())

    return values

def _find_offsets_matching_opcodes(co_code, opcodes):
    " Return a list of byte offsets inside co_code matching opcodes in 'opcodes' "
    return [idx * 2 for idx, opcode in enumerate(co_code[::2]) if opcode in opcodes]

def _find_abs_jump_offset_bytes(co_code):
    " Return a list of byte offets for jump offsets in co_code. "
    # Broken by EXTENDED ARG (if the argument is a jump offset)
    # idx + 1 returns the argument, rather than the bytecode.
    return [idx + 1 for idx in _find_offsets_matching_opcodes(co_code, ABS_JUMPS)]

def _rewrite_abs_jump_offsets(code_bytes, amt):
    " Add 'offset' to all jumps. "
    for offset in _find_abs_jump_offset_bytes(code_bytes):
        code_bytes[offset] += amt

def _extend_instr(opcode, arg):
    " Prefix opcode with one or more EXTENDED_ARG opcodes if it's > 255. "
    arg_bytes = []
    while True:
        arg_bytes.append(arg & 0xff)
        arg >>= 8
        if not arg:
            break

    code = []
    while len(arg_bytes) > 1:
        code.extend([EXTENDED_ARG, arg_bytes.pop()])

    code.extend([opcode, arg_bytes.pop()])
    return code

FRAME_CONST_IDX = -2
CODE_MAGIC_IDX = 3
def _resume(tb):
    """
    Main function for ON ERROR RESUME NEXT. Generate new callables for each frame in 'tb' and return the root callable.
    """
    if tb.tb_frame.f_code is sys.excepthook.__code__:
        # We're being called from the excepthook.
        return _resume(tb.tb_next)

    if tb.tb_frame.f_code.co_code.startswith(bytes([NOP, MAGIC, NOP])):
        # We've patched this function before. Restore the original traceback frame which we squirrelled away.
        tb_frame = tb.tb_frame.f_code.co_consts[FRAME_CONST_IDX]

        # Fix offets, which will include our patch prefix.
        old_prefix_length = tb.tb_frame.f_code.co_code[CODE_MAGIC_IDX]
        faulting_instruction_idx = tb.tb_lasti - old_prefix_length
    else:
        tb_frame = tb.tb_frame
        faulting_instruction_idx = tb.tb_lasti

    old_code_obj = tb_frame.f_code
    code_bytes = list(old_code_obj.co_code)

    if tb.tb_next:
        # This isn't the frame which caused the exception. This is a parent frame which called something which caused
        # the exception. We can't just re-try the call, though, because we want to call a rewritten child which skips
        # the exception-causing behaviour. So instead we skip to the next instruction here.
        child_callable, child_args = _resume(tb.tb_next)
        next_instr_idx = faulting_instruction_idx + 2
    else:
        # We're on the frame with the faulting instruction. Find the next line. The compiler can reorder lines, so this
        # isn't guaranteed to do anything sensible, but if you're looking for sensible you're in the wrong place.
        child_callable, child_args = None, None
        for offset, lineno in dis.findlinestarts(tb_frame.f_code):
            if offset > faulting_instruction_idx and lineno > tb_frame.f_lineno:
                next_instr_idx = offset
                break
        else:
            # We ran out of lines (e.g. last line of function was 'return <something which blows up>).
            # Fall back to resuming on the next opcode. The last opcode of every Python function is RETURN_VALUE,
            # which won't throw (assuming the stack isn't corrupt, which isn't a guarantee here actually :), so
            # doing this should be relatively safe.
            next_instr_idx = faulting_instruction_idx + 2

    # Create a short prefix which will fix up the code, starting with a magic sequence so we can identify
    # code we've modified
    prefix_code = [
        NOP, MAGIC,
        NOP, 0  # index of first instruction past our patch prefix, to be filled in later.
    ]

    if old_code_obj.co_varnames:
        # It's something which has a distinct locals() (i.e. a function). Supply them as arguments.
        argcount = len(tb_frame.f_code.co_varnames)
        args = [tb_frame.f_locals.get(name) for name in tb_frame.f_code.co_varnames]
    else:
        # It's something else (e.g. a module). Don't supply locals.
        argcount = 0
        args = []

    args.reverse()  # Args are written RTL.

    if faulting_instruction_idx >= 0:
        # Restore the value stack. The interpreter doesn't record the value stack depth in a very accessible way (it's a
        # local variable on the C stack in ceval.c), so figure out the depth of the stack using abstract interpretation.
        stack_depth = _get_value_stack_depth(code_bytes, faulting_instruction_idx)
        stack = _fetch_value_stack(tb_frame, stack_depth)  # first entry is bottom of stack.
    else:
        # The exception is coming from inside the house^W^W^Wour fixup stub code.
        print(tb.tb_lasti, faulting_instruction_idx, tb, tb.tb_next)
        raise NotImplementedError()

    # Add some magic values as consts.
    co_consts = list(old_code_obj.co_consts)

    # First magic const: the patched child function to call.
    child_callable_const_idx = None
    if child_callable:
        co_consts.append(child_callable)
        co_consts.append(child_args)
        child_callable_const_idx = len(co_consts) - 2

    # Second magic const: the original traceback frame. We use this to get the unpatched version of a function, should
    # the patched version throw another exception.
    co_consts.append(tb_frame)

    # Third magic const: the stack as a tuple.
    if tb.tb_next and stack and isinstance(stack[-1], ObliteratedByException):
        # Normally the result of an exception is NULL, but in this case we know the last thing we did in this
        # frame involved a function call (because tb_next is not None), and we've called the function above
        # and have a result. We will restore the stack and then call the function.
        stack = stack[:-1]

    co_consts.append(tuple(stack))

    # Add code to restore the stack from our const tuple when the function starts.
    if stack:
        prefix_code.extend([
            LOAD_CONST, len(co_consts) - 1,
            UNPACK_SEQUENCE, len(stack),
        ])

    # Add code to call the patched child function (if any) when the function starts.
    if child_callable:
        prefix_code.extend([
            LOAD_CONST, child_callable_const_idx,  # callable
            LOAD_CONST, child_callable_const_idx + 1,  # args
            UNPACK_SEQUENCE, len(child_args),
            CALL_FUNCTION, len(child_args)])

    # Add code to jump to where we left off in the function after we've restored its state.
    prefix_code.extend(_extend_instr(JUMP_ABSOLUTE, next_instr_idx))

    # We've finished adding code to the patch prefix, so store its length. We store it in the
    # otherwise-unused argument slot to the NOP opcode (in recent CPython versions, every opcode
    # has an argument slot).
    prefix_code[CODE_MAGIC_IDX] = len(prefix_code)

    # The new code is the previous code plus our prefix.
    code_bytes = prefix_code + code_bytes

    # Now that we've put the prefix code at the start, rewrite all absolute jumps.
    _rewrite_abs_jump_offsets(code_bytes, len(prefix_code))

    # We can now construct a full code object and function object with our new code and consts, using the original as a
    # template.
    co_names = old_code_obj.co_names
    print("co_names type:", type(co_names))
    new_code_obj = types.CodeType(argcount, 0,
                                  old_code_obj.co_kwonlyargcount, old_code_obj.co_nlocals,
                                  old_code_obj.co_stacksize, old_code_obj.co_flags, bytes(code_bytes),
                                  tuple(co_consts), co_names, old_code_obj.co_varnames,
                                  old_code_obj.co_filename, old_code_obj.co_name, old_code_obj.co_firstlineno,
                                  old_code_obj.co_lnotab)

    # TODO: __closure__ not copied
    frame_func = types.FunctionType(new_code_obj, tb_frame.f_globals, name=tb_frame.f_code.co_name)

    #print('resume called for tb ', tb, tb.tb_next, frame_func)
    #dis.dis(frame_func, depth=0)

    return (frame_func, tuple(args))

def _excepthook(type_, value, tb):
    global _last_error

    while True:
        _last_error.err = type_

        func, args = _resume(tb)
        try:
            func(*args)
        except Exception as e:
            type_, value, tb = sys.exc_info()
            #print('continuing...')
            #traceback.print_exc()
        else:
            break

def on_error_resume_next():
    sys.excepthook = _excepthook

def err():
    err = _last_error.err
    _last_error.err = None
    return err