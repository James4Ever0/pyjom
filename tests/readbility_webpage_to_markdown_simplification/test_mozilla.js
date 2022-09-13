const jsdom = require("jsdom");
const { JSDOM } = jsdom;
doc = new jsdom.JSDOM(``, {
    url: "https://www.baidu.com"
});
const { Readability } = require('@mozilla/readability');
let reader = new Readability(doc.window.document);
let article = reader.parse();
console.log(article.title);