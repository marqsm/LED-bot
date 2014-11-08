$(document).ready(function() {
    ajaxFormHandler("#text-form","/show-text/",function(data) {
      $("#reply").text(data);
    });

    ajaxFormHandler("#image-form","/show-image/",function(data) {
      $("#reply").text(data);
    });

    $("#color-picker").spectrum({
      color: "#007800",
      change: function(color) {
        var c = color.toRgb();
        var cFormat = c.r+","+c.g+","+c.b;
        $("#color-picker").val(cFormat);
      }               
    });

    $("#bg-picker").spectrum({
      color: "#000000",
      change: function(color) {
        var c = color.toRgb();
        var cFormat = c.r+","+c.g+","+c.b;
        $("#bg-picker").val(cFormat);
      }               
    });

  });

  function ajaxFormHandler(selector,dest,callback) {
    $(selector).on("submit",function(evt) {
      evt.preventDefault();
      $.ajax({ 
        type: "POST",
        url: dest,
        data: $(selector).serialize()
      })
      .done(function(data) { 
        callback(data);
      });
    });
  };