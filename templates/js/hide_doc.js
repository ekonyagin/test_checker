function myFunction(a) {
  var x = document.getElementById("target");
  var y = document.getElementById("target2");
  
  if (a == "target") {
	    x.style.display = "block";
	    y.style.display = "none";
} if (a == "target2") {
		x.style.display = "none";
	    y.style.display = "block";
}
}