
$.getJSON("/request_topics",
  function (json) {
      $.each(json,
      function (key, value) {
      console.log(key)
      console.log(value)
      $("#id-select").append("<option value='" + value.c + "'>" + value.d + "</option>");
      });
});


