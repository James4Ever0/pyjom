#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:    御风
# @Mail:      zhong.yufeng@foxmail.com
# @Time:      2022/5/9 16:02
# @Desc:      汇编代码处理


import os
import time
from utils.shell import execute

CURRENT_DIR = os.path.dirname(__file__)
NASM_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "../tools/nasm.exe"))
TMP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../tmp"))
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

ARCH_16 = 16
ARCH_32 = 32
ARCH_64 = 64
ARCH_SUPPORTED = [ARCH_16, ARCH_32, ARCH_64]


class Asm(object):

    def __init__(self, arch: int = ARCH_32):
        self.nasm = NASM_PATH
        self.tmp = TMP_DIR
        self.arch = arch
        self.code = list()

    def clean(self):
        self.code = list()

    def append(self, code: str):
        self.code.append(code)

    def build(self, code: str = None, clean: bool = True):
        """
        编译汇编代码
        :param code: 处理代码, 留空则使用缓存代码
        :param clean: 清除缓存代码
        :return:
        """
        asmCode = ""
        if isinstance(code, str) and code != "":
            asmArr = []
            for s in code.replace("\r", "\n").split("\n"):
                s = (s if ";" not in s else s.split(";", maxsplit=1)[0]).strip()
                if not bool(s):
                    continue
                asmArr.append(s)
            asmCode = "\n".join(asmArr)
        elif len(self.code) > 0:
            asmCode = "\n".join([s.strip() for s in self.code if bool(s)])
        if asmCode == "":
            return None
        asmCode = f"bits {self.arch}\n{asmCode}"

        t = int(time.time() * 1000000)
        inputFile = os.path.join(self.tmp, f"{t}.asm").replace("\\", "/")
        outputFile = os.path.join(self.tmp, f"{t}.out").replace("\\", "/")
        bytesCode = None
        try:
            with open(inputFile, "wb") as f:
                f.write(asmCode.encode())
            cmd = f"\"{NASM_PATH}\" -f bin \"{inputFile}\" -o \"{outputFile}\""
            ret = execute(cmd, timeout=10000)
            if ret.success and os.path.exists(outputFile):
                with open(outputFile, "rb") as f:
                    bytesCode = f.read()
        except Exception:
            pass
        finally:
            if not (isinstance(code, str) and code != "") and clean:
                self.code = list()
            if os.path.exists(inputFile):
                os.remove(inputFile)
            if os.path.exists(outputFile):
                os.remove(outputFile)
        return bytesCode


if __name__ == "__main__":
    pass

    asm = Asm(ARCH_32)
    code = asm.build("""
        MOV EAX, 0x00
        INC EAX
    """)
    print([c for c in code])

    # asm = Asm(ARCH_32)
    # code = asm.build("""
    #     MOV EAX, 0x7FFF00AB
    #     PUSH EAX
    # """)
    # print([c for c in code])

    # code = asm.build("""
    #     PUSH 0x7FFF00AB
    # """)
    # print(code)
    # print([c for c in code])
