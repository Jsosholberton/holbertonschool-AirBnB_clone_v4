$(document).ready(function () {
  const amenityData= {};
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
        stringData += ", "
      }
      stringData += amenityData[amenity]['name'];
    }

    $(".amenities h4").text(stringData);
    stringData = " ";

  });
});
