const SQUARE_MILES = 5
let currMatrix = []
const fishNames = ['Atlantic Mackerel', 'Bigeye Tuna', 'Longfin Mako Shark', 'Orange Roughy', 'Pacific Mackerel',
                   'Prionace glauca', 'Scalloped Hammerhead', 'Southern Bluefin Tuna', 'Swordfish', 'Yellowfin Tuna']

document.getElementById('predictForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    const latitude = parseFloat(document.getElementById('latitude').value);
    const longitude = parseFloat(document.getElementById('longitude').value);

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.prediction);
        currMatrix = data.prediction;
        initMap(data.prediction, longitude, latitude);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function initMap(severity_matrix, longitude = 0.0, latitude = 0.0) {
    // Long = x; Lat = y
    var center = {lat: latitude, lng: longitude};

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: center,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });


    const colors = chroma.scale(['green', 'lightgreen', 'yellow', 'orange', 'red', 'purple']).mode('rgb').colors(100);
    let sum = 0.0
    for (var i = 0; i < SQUARE_MILES; i++) {
        for (var j = 0; j < SQUARE_MILES; j++) {
            sum += severity_matrix[i][j];
        }
    }
    const avg = sum / 25.0
    updatePointer(avg);


    var circle = new google.maps.Circle({
        map: map,
        center: center,
        radius: 30000, // Radius in meters (30 kilometers, approximately 16 nautical miles)
        fillColor: colors[avg * 100],
        fillOpacity: 0.35,
        strokeColor: colors[avg * 100],
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    var infoWindow = new google.maps.InfoWindow({
        content:   `<div style="font-family: Arial, sans-serif; font-size: 14px; color: black; background-color: white; border-radius: 5px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                        <strong>Coordinates:</strong><br>
                        Latitude: ${center.lat.toFixed(2)}<br>
                        Longitude: ${center.lng.toFixed(2)}
                    </div>`,
    });

    circle.addListener('click', function() {
        infoWindow.setPosition(center);
        infoWindow.open(map);
    });

    var marker = new google.maps.Marker({
        position: center,
        map: map,
    });
}

function updatePointer(value) {
    const legendHeight = document.getElementById('legend-container').offsetHeight;
    const pointer = document.getElementById('pointer');
    const pointerValue = document.getElementById('pointer-value');
    const position = value * legendHeight;
    pointer.style.top = `${position}px`;
    pointerValue.textContent = value.toFixed(2);
}

function createFishButtons() {
    const container = document.getElementById('fishButtons');
    fishNames.forEach(name => {
        const button = document.createElement('button');
        button.className = 'fish-button';
        button.innerText = name;
        button.onclick = () => console.log(name);
        container.appendChild(button);
    });
}

document.addEventListener('DOMContentLoaded', createFishButtons);
