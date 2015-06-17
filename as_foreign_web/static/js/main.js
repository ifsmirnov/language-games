var quantiles = [
  [100000, "Все слова из книжки :)"],
  [12000, "Очень просто"],
  [7000, "Просто"],
  [3000, "Умеренно"],
  [1500, "Сложно"],
  [500, "Очень сложно"],
  [0, "Вы вообще знаете русский?"],
];

var last_request_time = 0;
var update_pending = false;
var seed = new Date().getTime();
var first_focus = true;

function update() {
  if (update_pending) {
    return;
  }
  update_pending = true;

  var delta = new Date().getTime() - last_request_time;
  if (delta < 0) {
    return;
  }
  if (delta > 2000) {
    doUpdate();
  } else {
    setTimeout(doUpdate, 2000 - delta)
  } 
}

function doUpdate() {
  update_pending = false;
  last_request_time = new Date().getTime();
  if ($("#input_text").val().length > 0) {
    $.post(
        "/text/",
        {
          data: $("#input_text").val(),
          top_k: quantiles[slider.getValue()][0],
          seed: seed,
        },
        function(data, status, some_unknown_shit) {
          if (data.length > 0) {
            $("#result").html(data);
          }
        }
    );
  }
}

$(document).ready(function() {
  slider = $("#top_k_slider").slider({
    min: 0,
    max: quantiles.length - 1,
    step: 1,
    value: 3,
    formater: function(value) {
      return quantiles[value][1];
    }
  })
  .on("slide", update)
  .data("slider")
  $("#input_text").on("change keyup paste", function() {
    update();
  });
  $("#input_text").on("focus", function() {
    if (first_focus) {
      $(this).val("");
      first_focus = false;
    }
  });
  update();
}); 
