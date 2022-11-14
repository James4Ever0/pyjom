import hy
# this is different. no a
print('message before repl')
repl = hy.cmdline.HyREPL()
repl.run()
print('message after repl')
