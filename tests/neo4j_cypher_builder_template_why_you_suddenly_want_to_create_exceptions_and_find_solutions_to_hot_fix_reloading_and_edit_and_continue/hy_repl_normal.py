import hy.cmdline
# this is different. no access to hidden member.
print('message before repl')
repl = hy.cmdline.HyREPL()
repl.run()
print('message after repl')

