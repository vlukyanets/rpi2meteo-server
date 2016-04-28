/* 2016 (C) Valentin Lukyanets */


function initMap() {
    var mapDiv = document.getElementById('gmap');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: 0.0, lng: 0.0},
        zoom: 3
    });
    return map
}


function getPosition(_data) {
    raw_position_object = _data['sensors']['Geolocation'][0];
    _data['sensors']['Geolocation'][0] = new google.maps.LatLng(
        raw_position_object.lat, raw_position_object.lng
    );
    return raw_position_object
}


function timestampToUtcStr(_timestamp) {
    console.log(_timestamp);
    return (new Date(1000 * _timestamp)).toUTCString();
}


function makeContent(_data) {
    var content = "<div>";
    content = "<h4>Device ID: ";
    content += _data['device_id'];
    content += "</h4><br>";
    content += "<ul>";
    var all_sensors = _data['sensors'];
    for (var sensor_name in all_sensors) {
        if (all_sensors.hasOwnProperty(sensor_name)) {
            content += "<li>";
            content += sensor_name;
            content += ": ";
            console.log(all_sensors[sensor_name][0]);
            content += all_sensors[sensor_name][0];
            content += " ";
            content += all_sensors[sensor_name][1];
            content += "</li><br>";
        }
    }
    content += "</ul><br>";
    content += "Last update: ";
    content += timestampToUtcStr(_data['time']);
    content += "<br>";
    content += "Watch history: ";
    content += '<a href="/device/' + _data['device_id'] + '">link</a>';
    content += "</div>";
    return content;
}


function addMarker(_map, _jsonMarkerData) {
    console.log('Invoked addMarker');
    var markerPosition = getPosition(_jsonMarkerData);
    var infoWindowContent = makeContent(_jsonMarkerData);
    console.log(markerPosition);

    var infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent
    });
    var marker = new google.maps.Marker({
        position: markerPosition,
        map: _map,
        visible: true,
    });
    marker.addListener('click', function() {
       infoWindow.open(_map, marker);
    });
    marker.setMap(_map);
}


function loadContent(_url) {
    var request = new XMLHttpRequest();
    request.open('GET', _url, false);
    request.send();
    if (request.status != 200) {
        alert("Data is inaccessible!");
        return [];
    } else {
        console.log(request.responseText);
        return JSON.parse(request.responseText);
    }
}
