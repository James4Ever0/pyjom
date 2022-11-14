import hy.cmdline
# this is different. no access to hidden member.
print('message before repl')
repl = hy.cmdline.HyREPL() # this is not reliable. exit will exit this shit for good.
repl.run()
print('message after repl')
# no message after repl?
