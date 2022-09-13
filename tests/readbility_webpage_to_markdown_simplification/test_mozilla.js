const jsdom = require("jsdom");
const { JSDOM } = jsdom;
doc =  jsdom(``, {
    url: "https://www.baidu.com"
});
const { Readability } = require('@mozilla/readability');
let reader = new Readability(doc.window.document);
let article = reader.parse();
console.log(article.title);