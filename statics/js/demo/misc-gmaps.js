
// Misc-Gmaps.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(document).ready(function() {


	// GMAPS
	// =================================================================
	// Require gmaps
	// -----------------------------------------------------------------
	// http://hpneo.github.io/gmaps/
	// =================================================================



	// Marker
	// =================================================================
	var markerMap = new GMaps({
		el: '#demo-marker-map',
		lat: 37.336095,
		lng: -121.8885431
	});
	markerMap.addMarker({
		lat: 37.336095,
		lng: -121.8885431,
		title: 'Location',
		click: function(e) {
			$.niftyNoty({
				type: "info",
				icon: "fa fa-info",
				message: "You clicked in the marker",
				container: 'floating',
				timer: 3500
			});
		},
		infoWindow: {
			 content: '<div>HTML Content</div>'
		}
	});





	// Street View Panoramas
	// =================================================================
	var panorama = GMaps.createPanorama({
		el: '#demo-panorama-map',
		lat: 37.336095,
		lng: -121.8885431
	});





	// Overlay
	// =================================================================
	var overlayMap = new GMaps({
		div: '#demo-overlays-map',
		lat: 37.336095,
		lng: -121.8885431
	});
	overlayMap.drawOverlay({
		lat: overlayMap.getCenter().lat(),
		lng: overlayMap.getCenter().lng(),
		content: '<div class="popover top" style="display:block; width:200px"><div class="arrow"></div><div class="popover-content"><strong>You are here</strong><p>1 Washington Sq, San Jose, CA 95192, United States</p></div></div>',
		verticalAlign: 'top',
		horizontalAlign: 'center'
	});





	// Map Type
	// =================================================================
	var mapType = new GMaps({
		div: '#demo-type-map',
		lat: 37.336095,
		lng: -121.8885431,
		mapTypeControlOptions: {
			mapTypeIds : ["hybrid", "roadmap", "satellite", "terrain", "osm", "cloudmade"]
		}
	});
	mapType.addMapType("osm", {
		getTileUrl: function(coord, zoom) {
			return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
		},
		tileSize: new google.maps.Size(256, 256),
		name: "OpenStreetMap",
		maxZoom: 18
	});
	mapType.addMapType("cloudmade", {
		getTileUrl: function(coord, zoom) {
			return "http://b.tile.cloudmade.com/8ee2a50541944fb9bcedded5165f09d9/1/256/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
		},
		tileSize: new google.maps.Size(256, 256),
		name: "CloudMade",
		maxZoom: 18
	});
	mapType.setMapTypeId("osm");






	// Geocoding
	// =================================================================
	var geomap = new GMaps({
		div: '#demo-geocoding-map',
		lat: -12.043333,
		lng: -77.028333
	});

	$('#demo-geocoding-form').submit(function(e){
		e.preventDefault();
		GMaps.geocode({
			address: $('#demo-geocoding-address').val().trim(),
			callback: function(results, status){
				if(status=='OK'){
					var latlng = results[0].geometry.location;
					geomap.setCenter(latlng.lat(), latlng.lng());
					geomap.addMarker({
						lat: latlng.lat(),
						lng: latlng.lng()
					})
				}
			}
		})
	})

});
