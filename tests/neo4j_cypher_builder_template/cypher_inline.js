var cypher = function(str) { return str; }
var sql = function(str) { return str; }
var a = cypher `create (n)-[:married]->(r)`; // well that's good.
console.log(a);
const query = sql `SELECT * FROM users`;
console.log(query);
// function otherfunc(){
//     console.log('calling otherfunc')
//     return 'other func'
// }
// function myfunc() {
//     otherfunc()
//     return query;
// }
// // __export__
// // console.log(module.loaded) // false
// // export all functions?
// module.exports = {otherfunc, myfunc} // also some bloated shit.
// which one you want? damn...
// you want some object?

// what if they are interdependent?

// this is some other strange shit.
// exports = {
//         otherfunc: () => {
//             console.log('calling otherfunc');
//             return 'otherfunc'
//         },
//         myfunc: () => {
//             exports.otherfunc() // strange shit.
//             return query;
//         }
//     }
//     // console.log(module)
// module.exports = exports // must use this to export things.

// this is self-reference.

class Query {
    constructor(a, b) {
        this.a = a
        this.b = b
    }
    static otherfunc() {
        // otherfunc() {
        console.log('calling otherfunc');
        return 'otherfunc'
    }
    static myfunc() {
        // static myfunc() {
        Query.otherfunc() // strange shit.
        // this.otherfunc() // still working for static functions.
        // javascript is a beast.
        return query;
    }
}
module.exports = { Query }
// console.log(.cypher)
console.log(this.Query)