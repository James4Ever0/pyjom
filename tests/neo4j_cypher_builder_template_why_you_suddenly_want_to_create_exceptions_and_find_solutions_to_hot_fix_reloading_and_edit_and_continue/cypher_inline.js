
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals

// official javascript driver
// https://neo4j.com/developer/javascript/
var cypher = function(strArray, ...opts) { // this is bad.
    console.log('input:', strArray, opts) // here we've got the thing.
    // passed here. good.
    // this will be good.
    // suppose we put string, object into this thing.
    // suppose we quote the thing.
    return strArray;
}
var sql = function(str) { return str; }
var myexpression = {obj:2}; // not supplied to cypher?
// create (n)-[:married]->(r) [object Object]
// wtf?
var myexpression2 = '3';
var b = `create (n)-[:married]->(r) ${myexpression}`
console.log(b) // create (n)-[:married]->(r) 2
    // this will format the thing.
var a = cypher `create (n:person{name:${myexpression}})-[:married]->(r) ${myexpression2}`; // well that's good.
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
    static myfunc(...args) {
        // static myfunc() {
            console.log('myfunc args:',args)
        Query.otherfunc() // strange shit.
            // this.otherfunc() // still working for static functions.
            // javascript is a beast.
        return query;
    }
}
module.exports = { Query }
    // console.log(.cypher)
    // console.log('QUERY?',globalThis.Query, this.sql) // all undefinded.