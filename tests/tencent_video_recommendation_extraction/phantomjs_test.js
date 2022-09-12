var page = require('webpage').create();
page.open('http://v.qq.com/x/page/m0847y71q98.html', function(status) {
	//console.log("Status: " + status);
	if(status === "success") {
	//	page.render('example.png');
		result = page.evaluate(()=>document.body.innerHTML);
		console.log(result)
	}
	phantom.exit();
});
