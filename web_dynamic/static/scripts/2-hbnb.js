$(document).ready(function () {
  const amenityData = {};
  var stringData = " ";

  $('input[type="checkbox"]').change(function () {
    const checkbox = $(this);
    const amenityID = checkbox.data("id");
    const amenityName = checkbox.data("name");

    if (checkbox.is(":checked")) {
      amenityData[amenityID] = { id: amenityID, name: amenityName };
    } else {
      delete amenityData[amenityID];
    }

    for (const amenity in amenityData) {
      if (stringData !== " ") {
        stringData += ", ";
      }
      stringData += amenityData[amenity]["name"];
    }

    $(".amenities h4").text(stringData);
    stringData = " ";
  });

  const url = "http://127.0.0.1:5001/api/v1/status/";

  $.ajax({
    url: url,
    method: "GET",
    complete: function (req) {
      if (req.status == 200) {
        $("div#api_status").addClass("available");
      } else {
        $("div#api_status").removeClass("available");
      }
    },
  });
});
