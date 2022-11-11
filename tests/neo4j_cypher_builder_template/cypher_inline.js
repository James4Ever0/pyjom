var cypher = function(str) { return str; }
var sql = function(str) { return str; }
var a = cypher `create (n)-[:married]->(r)`; // well that's good.
console.log(a);
const query = sql `SELECT * FROM users`;
console.log(query);
// function otherfunc(){
//     console.log('calling otherfunc')
// }
// function myfunc() {
//     otherfunc()
//     return query;
// }
// __export__
// console.log(module.loaded) // false
// export all functions?
// module.exports = 

// what if they are interdependent?

module.exports = {
        otherfunc: () => {
            console.log('calling otherfunc');
        },
        myfunc: () => {
            otherfunc()
            return query;
        }
    }
    // console.log(module)