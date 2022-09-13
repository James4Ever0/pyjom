var { Readability } = require('@mozilla/readability');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
var doc = new JSDOM(``, {
  url: "https://www.baidu.com"
});
let reader = new Readability(doc.window.document);
let article = reader.parse();
console.log(article.title);