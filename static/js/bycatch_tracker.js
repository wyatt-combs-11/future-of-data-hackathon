const SQUARE_MILES = 40

function initMap() {
    var center = {lat: 37.7749, lng: -122.4194}; // Example: San Francisco

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: center,
    });

    var squareSize = 1 * 1609.34; // 1 mile in meters
    var startLat = center.lat + 0.0145 * (SQUARE_MILES / 2);
    var startLng = center.lng - 0.0145 * (SQUARE_MILES / 2);

    var colors = chroma.scale(['green', 'yellow', 'orange', 'red', 'purple']).colors(100);

    for (var i = 0; i < SQUARE_MILES; i++) {
        for (var j = 0; j < SQUARE_MILES; j++) {
            var bounds = {
                north: startLat - i * 0.0145, // Move south
                south: startLat - (i + 1) * 0.0145, // Move south
                east: startLng + j * 0.0145, // Move east
                west: startLng + (j - 1) * 0.0145 // Move east
            };

            var colorIndex = Math.floor((i * SQUARE_MILES + j) * (100 / (SQUARE_MILES * SQUARE_MILES)));
            colorIndex = Math.min(99, Math.max(0, colorIndex + Math.floor(Math.random() * 5 - 2)));

            var fillColor = colors[colorIndex];

            var rectangle = new google.maps.Rectangle({
                strokeColor: '#000000',
                strokeOpacity: 0.5,
                strokeWeight: 1,
                fillColor: fillColor,
                fillOpacity: 0.5,
                map: map,
                bounds: bounds
            });
        }
    }
}
