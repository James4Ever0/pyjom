a = "select * from user"


b = "create (n:person)"  # cypher # not working!
from javascript import require, globalThis

chalk = require(
    "./cypher_inline.js"
)  # that might be some drop-in replacement for jinja? should they work together?

# print(dir(chalk))
# what the fuck?
val = chalk.myfunc()
print("VALUE", list(val), type(val))  # it can be converted.
val = chalk.otherfunc()
print("VALUE", val, type(val))  # it can be converted.
