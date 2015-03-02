var socket = io();

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
	osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib}),
	map = new L.Map('map', {layers: [osm], center: new L.LatLng(-37.7772, 175.2756), zoom: 15 });

var userMarker = null;
socket.on('newGpsPoint', function(newGpsPoint){
	latlngPoint = new L.Latlng(newGpsPoint.lattitude, newGpsPoint.longitude);
	if (userMarker === null){
		userMarker = new L.Marker(latlngPoint);
		userMarker.addTo(map);
		map.setView({center: latlngPoint, zoom: 15});
	} else {
		userMarker.setLatLng(latlngPoint);
	}
});

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
	draw: {
		position: 'topleft',
		polygon: {
			title: 'Draw a sexy polygon!',
			allowIntersection: false,
			drawError: {
				color: '#b00b00',
				timeout: 1000
			},
			shapeOptions: {
				color: '#bada55'
			},
			showArea: true
		},
		polyline: false,
		circle: false,
		marker: false
	},
	edit: {
		featureGroup: drawnItems
	}
});
map.addControl(drawControl);

map.on('draw:created', function (e) {
	var type = e.layerType,
		layer = e.layer;

	if (type === 'polygon') {
		var latlngs = layer.getLatLngs();
		notifyServerPolygonPoints(latlngs);
	}
});
map.on('draw:edited', function(e){
	var type = e.layerType,
		layer = e.layer;

	if (type === 'polygon') {
		var latlngs = layer.getLatLngs();
		notifyServerPolygonPoints(latlngs);
	}
});
map.on('draw:deleted', function(e){
	var type = e.layerType,
		layer = e.layer;
		
	if (type === 'polygon') {
		var latlngs = [];
		notifyServerPolygonPoints(latlngs);
	}
});
function notifyServerPolygonPoints(latlngs){
	console.log('new lat longs: ', latlngs);
	socket.emit('newPolygonPoints', latlngs);
}

socket.on('pointInPolygon', function(isPointInPolygon){
	if (isPointInPolygon){
		//change color of polygon shape to green
		drawControl.setDrawingOptions({
			polygon: {
				shapeOptions: {
					color: '#336600'
				}
			}
		});
	} else {
		//change color of polygon shape to red
		drawControl.setDrawingOptions({
			polygon: {
				shapeOptions: {
					color: '#CC3300'
				}
			}
		});		
	}
});
		
