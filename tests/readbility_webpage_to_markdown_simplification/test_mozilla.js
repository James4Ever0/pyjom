// const jsdom = require("jsdom");
// const { JSDOM } = jsdom;
// doc = new jsdom.JSDOM(``, {
//     url: "https://www.baidu.com"
// });

document=`

`

const { Readability } = require('@mozilla/readability');
let reader = new Readability(document);
let article = reader.parse();
console.log(article.title);