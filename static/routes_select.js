var body = document.getElementsByTagName("body")[0];
var form = document.createElement("form");
form.id = "submit_line";
form.action = '/search/submit_route';
//form.method = "get";

$.getJSON("/search/request_routes", function(result){
	$.each(result, function(i, field){
		var line = i;
		//console.log(field);
		$.each(field, function(route, descr){
			console.log("Line" + i);
			console.log(route);
			console.log(descr);
			var DepTime = descr.dep;
			var ArrTime = descr.arr;
			var busRouteId = descr.busRouteId;

			var inp = document.createElement("input");
			inp.type = "radio";
			inp.name = 'route';
			inp.value = busRouteId;
			inp.id = busRouteId;
			form.appendChild(inp);
			//document.createTextNode("Departs at" + DepTime+'. Arrives at' +ArrTime);
			document.createElement("br");
			form.appendChild(document.createTextNode("Route "+busRouteId+". Departs at " + DepTime+'. Arrives at ' +ArrTime));
			form.appendChild(document.createElement("br"));
		});
	});
	var inp = document.createElement("input");
	inp.type = "submit";
	inp.value = "Select";
	inp.className="btn btn-primary"
	form.appendChild(inp);
	body.appendChild(form);
});


