fetch("/get_map_data")
  .then((response) => response.json())
  .then((data) => {
    if (data.success) {
      for (let i = 0; i < data.data.length; i++) {
        let row = data.data[i];
        var marker = L.marker([row.lat, row.lon]).addTo(map);
        marker
          .bindPopup(
            `<b>Area :</b> ${row.place}<br><b>POWER : </b>${row.power.toFixed(
              3
            )} KWatts.`
          )
          .openPopup();
        console.log(
          `Row ${i + 1}: Place=${row.place}, State=${row.state}, Lat=${
            row.lat
          }, Lon=${row.lon}, Power=${row.power}`
        );
      }
    } else {
      console.error("Error fetching map data:", data.message);
    }
  })
  .catch((error) => {
    console.error("Error fetching map data:", error);
  });

$(document).ready(function () {
  $("#states").change(function () {
    var selectedState = $(this).val();
    $.ajax({
      url: "/get_places/" + selectedState,
      type: "GET",
      success: function (data) {
        $("#places").empty();
        $.each(data.places, function (index, value) {
          $("#places").append(
            '<option value="' + value + '">' + value + "</option>"
          );
        });
      },
    });
  });

  document.getElementById("clearButton").addEventListener("click", function () {
    // Send a POST request to the /clear_map_data route
    fetch("/clear_map_data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert(data.message);
          // Optionally, you can refresh the page or update the map display
          // location.reload();
          // updateMapDisplay();
        } else {
          alert("Error clearing map data");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred");
      });
  });

  $("#submitBtn").click(function () {
    var selectedPlace = $("#places").val();
    var selectedState = $("#states").val();
    console.log("Selected Place:", selectedPlace);
    console.log("Selected State:", selectedState);

    $.ajax({
      url: "/get_coordinates",
      type: "POST",
      data: { place: selectedPlace, state: selectedState },
      success: function (data) {
        console.log("Server Response:", data);

        if ("lat" in data && "lon" in data && "power" in data) {
          alert(data.lat);
        } else {
          alert("Coordinates not found");
        }
      },
    });
  });
});

var mapOptions = {
  center: [23.543844826108984, 84.2266845],
  zoom: 5,
  zoomControl: false,
};
var map = new L.map("maps", mapOptions);
var layer = new L.TileLayer(
  "http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/ {y}.png"
);

map.addLayer(layer);
