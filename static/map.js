let map = L.map('mapid').setView([35.2271, -80.8431], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 2,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

//Show marker for each event location
for (let i = 0; i < eventData.length; i++) {
    let event = eventData[i];
    L.marker([event.latitude, event.longitude]).addTo(map)
        .bindPopup(event.title + ': ' + event.description + '<br>' + '<a href="/event/' + event.id + '">View Event</a>');
}

//Get user location
let userLocation = null;
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        map.setView([position.coords.latitude, position.coords.longitude], 16);
    });
}