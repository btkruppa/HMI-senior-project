// handlers.js

var main = $("#main-content");

var handlers = [
	["/EditElement/.*", editHandler],
	["/NewElement", editHandler],
	["/EditFeed/.*", feed2Handler],
	["/feed/.*", feedHandler],
	["/screen/.*", screenHandler],
	["/NewFeed", feedHandler],
	["/.*", pageHandler],
	[".*", indexHandler]
];

function hasher() {
	var title = window.location.hash.substr(1).replace(/\//g," | ").replace(/_/g," ").replace(/\./g," ").capitalize();
	document.title = config.title + title;

	var hash = window.location.hash.substr(1);
	for (var h in handlers) {
		var path = handlers[h][0].replace(/\//g,"\\\/");
		var r = new RegExp(path);
		var m = hash.match(path);
		if (m && m[0] === hash) {
			m = path.split("\\\/");
			hash = hash.split("/").filter(function(i) { return m.indexOf(i) < 0; });
			handlers[h][1].apply(this, hash);
			return true;
		}
	}
}

function indexHandler() {
  loader(main, "static/html/main.html", function() {
		// put after loading scripts here
	});
  if (window.location.hash.length > 1) {
    window.location.hash = "";
  }
}

function pageHandler(path1, path2) {
  var path = path1+(path2 ? "/"+path2 : "")+".html";
  loader(main, "static/html/"+path, function(xhr) {
    if (xhr.status > 400)
      window.location.href = "#";
  });
}



var getIdent;
function editHandler(id){
	loader(main, "static/html/NewElement.html", function() {
	});
	function getID(){
		var ident = id;
		return ident;
	}
	getIdent = getID;
}

var feedId;
function feedHandler(id) {
	loader(main, "static/html/NewFeed.html", function() {});
	function getID() {
		return id;
	}
	feedId = getID;
}

var screenId;
function screenHandler(id){
	loader(main, "static/html/Screen.html", function() {});
	function getID() {
		return id;
	}
	screenId = getID;
}

function feed2Handler(id) {
	loader(main, "static/html/feed.html", function() {});
}
