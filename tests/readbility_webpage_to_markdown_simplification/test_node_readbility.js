var read = require('node-readability');
url="https://zhuanlan.zhihu.com/p/384614837"
// 'http://howtonode.org/really-simple-file-uploads'
read(url, function(err, article, meta) {
    // Main Article
    console.log(article.content);// still html
    // Title
    console.log(article.title);
    console.log(article.textContent);
    console.log(article.lang);

    // HTML Source Code
    // console.log(article.html);
    // // DOM
    // console.log(article.document);

    // Response Object from Request Lib
    // console.log(meta);

    // Close article to clean up jsdom and prevent leaks
    article.close();
});