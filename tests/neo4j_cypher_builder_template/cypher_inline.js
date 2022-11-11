var cypher = function(str) { return str; }
var sql = function(str) { return str; }
var a = cypher `create (n)-[:married]->(r)`; // well that's good.
console.log(a);
const query = sql `SELECT * FROM users`;
console.log(query);

function myfunc() {
    return query;
}
// __export__
// console.log(module.loaded) // false
// module.exports = { myfunc: myfunc }