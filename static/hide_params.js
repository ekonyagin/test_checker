$(function() {
  
  // Get the form fields and hidden div
  var checkbox = $("#trigger");
  var hidden_exp = $("#div_exp");
  var hidden_fps = $("#div_fps");
  var hidden_roi = $("#div_roi");
  var text_fps = $("#text_fps");
  var text_exp = $("#text_exp");
  var text_roi = $("#text_roi");
  console.log("changed");
  //var text = document.getElementById("text");
  
  // Hide the fields.
  // Use JS to do this in case the user doesn't have JS 
  // enabled.
  hidden_exp.hide();
  hidden_fps.hide();
  hidden_roi.hide();
  text_exp.hide();
  text_fps.hide();
  text_roi.hide();
  // Setup an event listener for when the state of the 
  // checkbox changes.
  checkbox.change(function() {
    // Check to see if the checkbox is checked.
    // If it is, show the fields and populate the input.
    // If not, hide the fields.
    console.log("changed");
    if (checkbox.is(':checked')) {
      // Show the hidden fields.
      hidden_exp.show();
      hidden_fps.show();
      hidden_roi.show();
      text_exp.show();
      text_fps.show();
      text_roi.show();
      //text.style.display = "block";
      // Populate the input.
      //populate.val("Dude, this input got populated!");
    } else {
      // Make sure that the hidden fields are indeed
      // hidden.
      hidden_exp.hide();
      hidden_fps.hide();
      hidden_roi.hide();
      text_exp.hide();
      text_fps.hide();
      text_roi.hide();
      // You may also want to clear the value of the 
      // hidden fields here. Just in case somebody 
      // shows the fields, enters data to them and then 
      // unticks the checkbox.
      //
      // This would do the job:
      //
      $("#cam_exp").val("");
      $("#cam_fps").val("");
      $("#roi").val("");
    }
  });
});