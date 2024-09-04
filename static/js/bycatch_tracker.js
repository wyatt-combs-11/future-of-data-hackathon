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
        button.onclick = () => showFishInfo(name);
        container.appendChild(button);
    });
}

function showFishInfo(species) {
    document.getElementById('fishInfoLabel').innerText = species;
    document.getElementById('fishInfoText').innerText = "General Info:\n" + species_data[species][0] + "\n\nAvoiding Bycatch:\n" + species_data[species][1];
    var myModal = new bootstrap.Modal(document.getElementById('fishInfoModal'));
    myModal.show();
}

const species_data = {
    'Atlantic Mackerel': [
        'A fast-swimming species found in the North Atlantic, Atlantic mackerel is commonly used in commercial fishing. They are highly migratory, moving in schools.',
        'To reduce bycatch, using selective trawling nets and avoiding their peak migration seasons can help. Bycatch reduction devices (BRDs) are also effective.'],
    'Bigeye Tuna': [
        'Bigeye tuna is a prized species for both commercial and recreational fishing. Found in tropical and subtropical waters, they are often caught using longlines.',
        'One method to minimize bycatch is using circle hooks instead of J-hooks to prevent unintended captures of other species like sharks. Deploying gear at depths that specifically target the depth range where Bigeye Tuna swim is also recommended.'],
    'Longfin Mako Shark': [
        'A highly migratory species, the longfin mako shark is considered vulnerable due to overfishing and bycatch. They are often caught in tuna and swordfish longline fisheries.',
        'Shark-safe longline gear with circle hooks and avoiding fishing in known mako habitats during their peak season are helpful measures.'],
    'Orange Roughy': [
        'This deep-sea fish is highly vulnerable to overfishing due to its slow growth and late maturity. It is often caught by bottom trawlers.',
        'Using midwater trawls instead of bottom trawls can help reduce orange roughy bycatch. Avoiding known deep-sea habitats during spawning can also prevent their accidental capture.'],
    'Pacific Mackerel': [
        'Similar to Atlantic mackerel, Pacific mackerel are fast swimmers and are found along the coasts of the Pacific Ocean. They are widely targeted by purse seines.',
        'Modified purse seine nets and the use of fish aggregating devices (FADs) can help reduce bycatch when targeting other species in the same waters.'],
    'Prionace glauca': [
        'The blue shark, a highly migratory species, is one of the most commonly caught sharks in pelagic longline fisheries. They play a crucial role in marine ecosystems.',
        'Using shark deterrents like magnets or electropositive metals on hooks can minimize blue shark bycatch. Circle hooks also help prevent accidental capture.'],
    'Scalloped Hammerhead': [
        'This shark species is critically endangered due to overfishing and bycatch. They are often caught by longline fisheries targeting tuna and swordfish.',
        'Gear modifications like using weaker hooks that release hammerheads but retain larger fish can help. Setting lines deeper and outside of their habitat zones also reduces bycatch.'],
    'Southern Bluefin Tuna': [
        'Southern bluefin tuna are found mainly in the southern hemisphere and are highly prized in commercial fisheries. They are overfished and listed as critically endangered.',
        'Avoiding fishing during their spawning season and using selective longline methods are essential. Electronic tracking systems that monitor their movements can also aid in targeted fishing without bycatch.'],
    'Swordfish': [
        'Swordfish are large predatory fish found in tropical and temperate waters. They are primarily caught by longline and harpoon fisheries.',
        'To minimize bycatch, using specialized circle hooks and regulating the depth at which lines are set can target swordfish more effectively while avoiding other species like sharks or turtles.'],
    'Yellowfin Tuna': [
        'Yellowfin tuna are a popular species for commercial and sport fishing, found in tropical and subtropical waters. They are often caught using purse seines and longlines.',
        'Using dolphin-safe fishing techniques, like selective purse seining, can help prevent bycatch of marine mammals and other species. Bycatch reduction devices are also effective for Yellowfin Tuna fisheries.']
};

document.addEventListener('DOMContentLoaded', createFishButtons);
