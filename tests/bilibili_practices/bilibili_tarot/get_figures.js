var figures = document.getElementsByTagName("figure");
var mlinks = []
for (var fig of figures) {
    var link = fig.getElementsByTagName("img")[0].getAttribute("data-src").split("@")[0].replace("//", "https://");
    mlinks.push(link)
}
console.log(JSON.stringify(mlinks));