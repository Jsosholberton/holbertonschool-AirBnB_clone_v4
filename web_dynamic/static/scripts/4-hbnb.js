$(document).ready(function () {

  const amenityData = {};
  var stringData = " ";
  const amty_dict = {};

  const placesSection = $('section.places');

  function loadInitialData() {
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/places_search',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(amty_dict),
      success: function (data) {
        displayPlaces(data);
      },
      error: function (error) {
        console.error('Error:', error);
      }
    });
  }

  function displayPlaces(places) {
    placesSection.empty();
    places.sort(function (a, b) {
      return a.name.localeCompare(b.name);
    });
    places.forEach(function (place) {
      const article = $('<article>');
      article.html(`
      <div class="headline">
          <h2>${place.name}</h2>
          <div class="price_by_night">$${place.price_by_night}</div>
      </div>
      <div class="information">
          <div class="max_guest">
              <div class="guest_icon"></div>
              <p>${place.max_guest} Guests</p>
          </div>
          <div class="number_rooms">
              <div class="bed_icon"></div>
              <p>${place.number_rooms} Bedroom</p>
          </div>
          <div class="number_bathrooms">
              <div class="bath_icon"></div>
              <p>${place.number_bathrooms} Bathroom</p>
          </div>
      </div>
      <div class="user"><b>Owner</b>: ${place.user.first_name} ${place.user.last_name}</div>
      <div class="description">
          <p>${place.description}</p>
      </div>
  `);
      placesSection.append(article);
    });
  }

  loadInitialData();

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
    amty_dict["amenities"] = Object.keys(amenityData);
    callAPIWithFilters();
  });

  function callAPIWithFilters() {
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/places_search',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(amty_dict),
      success: function (data) {
        displayPlaces(data);
      },
      error: function (error) {
        console.error('Error:', error);
      }
    });
  }

  $.ajax({
    url: "http://127.0.0.1:5001/api/v1/status/",
    method: "GET",
    complete: function (req) {
      if (req.status == 200) {
        $("div#api_status").addClass("available");
      } else {
        $("div#api_status").removeClass("available");
      }
    },
  });
})
