// extracted from leaflet.geometryutil.js because it didn't work otherwise (0.3.2 incompatible with Leaflet 0.7.3?)
function rotatePoint(map, latlngPoint, angleDeg, latlngCenter) {
    var maxzoom = map.getMaxZoom();
    if (maxzoom === Infinity)
        maxzoom = map.getZoom();
    var angleRad = angleDeg*Math.PI/180,
        pPoint = map.project(latlngPoint, maxzoom),
        pCenter = map.project(latlngCenter, maxzoom),
        x2 = Math.cos(angleRad)*(pPoint.x-pCenter.x) - Math.sin(angleRad)*(pPoint.y-pCenter.y) + pCenter.x,
        y2 = Math.sin(angleRad)*(pPoint.x-pCenter.x) + Math.cos(angleRad)*(pPoint.y-pCenter.y) + pCenter.y;
    return map.unproject(new L.Point(x2,y2), maxzoom);
}

// http://cwestblog.com/2011/07/25/javascript-string-prototype-replaceall/
String.prototype.replaceAll = function(target, replacement) {
  return this.split(target).join(replacement);
};

function init(mapId, selectedEventKey) {
	var map = L.map(mapId);

	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
		maxNativeZoom: 19,
		maxZoom: 23
	}).addTo(map);

	var rainbow = new Rainbow().setSpectrum('green', 'red', 'blue');
	var markers = [];
	var overlays = {};
	var utcToLocalTimeOffset = new Date().getTimezoneOffset() * 60 * 1000;
	var utcToSingoporeTimeOffset = 8 * 60 * 60 * 1000;

	var popupTemplate = '\
		<div class="videoinfo">\
			<p class="title">${videoKey}</p>\
			<p>${date}</p>\
			<img src="../thumbnails/${videoKey}.jpg" width="200px"/>\
			<p>\
				Accuracy: ${acc}<br/>\
				<a href="http://liubei.ddns.comp.nus.edu.sg/jiku/dataset/download/datasets/${eventKey}/${videoKey}.mp4">Video</a>\
			</p>\
		</div>';

	for (var eventKey in locations) {
		// if an event is specified, filter out all other events
		if(selectedEventKey != null && selectedEventKey != eventKey) {
			continue;
		}

		var event = locations[eventKey];
		var eventMarkers = [];
		for(var videoKey in event) {
			var video = event[videoKey];
			console.log(videoKey + ': ' + video);
			var position = L.latLng(video.location.lat, video.location.lon);
			var direction = L.latLng(video.location.lat + 0.001, video.location.lon);
			direction = rotatePoint(map, direction, video.dir, position);
			//L.marker(position).addTo(map);
			var polyline = L.polyline([position, direction], {color: 'red', weight: 2});
			var circle = L.circle(position, 1, {color: '#'+rainbow.colourAt(video.location.acc)}).bindPopup(popupTemplate
				.replaceAll('${eventKey}', eventKey)
				.replaceAll('${videoKey}', videoKey)
				.replaceAll('${acc}', (video.location.acc).toFixed(1))
				.replaceAll('${date}', new Date(video.start + utcToLocalTimeOffset + utcToSingoporeTimeOffset).toLocaleString())
				);
			markers.push(L.marker(position));
			eventMarkers.push(circle);
			eventMarkers.push(polyline);
		}
		overlays[eventKey] = L.featureGroup(eventMarkers);
	}

	if(selectedEventKey == null) {
		var group = L.featureGroup(markers);
		map.fitBounds(group.getBounds().pad(0.2));

		overlaysLinks = {};
		for(layerName in overlays) {
			overlaysLinks['<a href="#" class="eventselector">' + layerName + '</a>'] = overlays[layerName];
		}

		L.control.layers(null, overlaysLinks, {collapsed: false}).addTo(map);

		$('#map').delegate('.eventselector', 'click', function() {
			console.log('click on ' + this.innerHTML);
			var layer = overlays[this.innerHTML];
			map.fitBounds(layer.getBounds());
			layer.addTo(map);
		});
	} else {
		overlays[selectedEventKey].addTo(map);
		map.fitBounds(overlays[selectedEventKey].getBounds().pad(0.2));
	}

	L.control.scale().addTo(map);
}