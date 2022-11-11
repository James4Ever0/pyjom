a = "select * from user"


b = "create (n:person)"  # cypher # not working!
from javascript import require, globalThis

chalk = require(
    "./cypher_inline.js"
)  # that might be some drop-in replacement for jinja? should they work together?

# print(dir(chalk))
# what the fuck?
q = chalk.Query(1,2)
# q = chalk.Query(1,2)
val = q.myfunc() # this is similar to the original shit.
# val = chalk.myfunc()
print("VALUE", list(val), type(val))  # it can be converted.
val = q.otherfunc()
# val = chalk.otherfunc()
print("VALUE", val, type(val))  # it can be converted.
