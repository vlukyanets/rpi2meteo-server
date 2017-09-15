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
    var raw_position_object = _data['sensors']['Geolocation'][0];
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
    content += "<h4>Device ID: ";
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


function dumpContentToTable(_content, _tableName) {
    var tableHtml = '<table border=1 width=100%>';
    for (var content_item_num in _content) {
        if (_content.hasOwnProperty(content_item_num)) {
            var content_item = _content[content_item_num];
            var sensors = content_item["sensors"];
            tableHtml += "<tr><td>";
            tableHtml += timestampToUtcStr(content_item["time"]);
            tableHtml += "</td><td>";
            for (var sensor_name in sensors) {
                if (sensors.hasOwnProperty(sensor_name)) {
                    tableHtml += sensor_name;
                    tableHtml += ": ";
                    tableHtml += presentationOf(sensors[sensor_name][0]);
                    tableHtml += " ";
                    tableHtml += sensors[sensor_name][1];
                    tableHtml += ";  ";
                }
            }
            tableHtml += "</td></tr>";
        }
    }
    tableHtml += '</table>';

    var tableElement = document.getElementById(_tableName);
    tableElement.innerHTML = tableHtml;
}


function presentationOf(_data) {
    if (typeof _data == 'object') {
        var s = "(";
        for (var subitem in _data) {
            s += _data[subitem];
            s += ";";
        }
        s += ")";
        return s;
    } else {
        return _data;
    }
}
