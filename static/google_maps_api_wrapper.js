/* 2016 (C) Valentin Lukyanets */


function initMap() {
    var mapDiv = document.getElementById('gmap');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: 0.0, lng: 0.0},
        zoom: 0
    });
    return map
}


function getPosition(_data) {
    return _data['sensors']['Geolocation'];
}


function timestampToUtcStr(_timestamp) {
    return (new Date(_timestamp)).toUTCString();
}


function makeContent(_data) {
    var content = "<div>";
    content = "<h4>Device ID: ";
    content += _data['device_id'];
    content += "</h4><br>";
    content += "<ul>";
    var all_sensors =  _data['sensors'];
    for (var sensor_name in all_sensors) {
        if (all_sensors.hasOwnProperty(sensor_name)) {
            content += "<li>";
            content += sensor_name;
            content += ": ";
            content += all_sensors[sensor_name][0];
            content += " ";
            content += all_sensors[sensor_name][1];
            content += "</li><br>";
        }
    }
    content += "</ul><br>";
    content += "Last update: ";
    content += timestampToUtcStr(_data['time']);
    content += "</div>";
    return content;
}


function addMarker(_map, _jsonMarkerData) {
    var markerPosition = getPosition(_jsonMarkerData);
    var infoWindowContent = makeContent(_jsonMarkerData);

    var infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent
    });
    var marker = new google.maps.Marker({
        position: markerPosition,
        map: _map
    });
    marker.addListener('click', function() {
       infoWindow.open(_map, marker);
    });
}


function loadContent(_url) {
    var request = new XMLHttpRequest();
    request.open('GET', _url, false);
    request.send();
    if (request.status != 200) {
        alert("Data is inaccessible!");
        return '';
    } else {
        return request.responseText;
    }
}
