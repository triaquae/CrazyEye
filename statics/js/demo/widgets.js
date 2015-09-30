
// Widgets.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).ready(function() {


	// REALTIME FLOT CHART
	// =================================================================
	// Require Flot Charts
	// -----------------------------------------------------------------
	// http://www.flotcharts.org/
	// =================================================================
	// We use an inline data source in the example, usually data would
	// be fetched from a server

	var data = [],  totalPoints = 300;

	function getRandomData() {
		if (data.length > 0)
			data = data.slice(1);

		// Do a random walk

		while (data.length < totalPoints) {
			var prev = data.length > 0 ? data[data.length - 1] : 50,
				y = prev + Math.random() * 10 - 5;

			if (y < 0) {
				y = 0;
			} else if (y > 100) {
				y = 100;
			}

			data.push(y);
		}

		// Zip the generated y values with the x values
		var res = [];
		for (var i = 0; i < data.length; ++i) {
			res.push([i, data[i]])
		}
		return res;
	}

	// Set up the control widget
	var updateInterval = 1000;
	var flotOptions = {
		series: {
			lines: {
				lineWidth:0,
				show: true,
				fill: true,
				fillColor : "#c2a1be"
			},
			shadowSize: 0	// Drawing is faster without shadows
		},
		yaxis: {
			min: 0,
			max: 110,
			ticks: 30,
			show: false
		},
		xaxis: {
			show: false
		},
		grid: {
			hoverable: true,
			clickable: true,
			borderWidth: 0
		},
		tooltip: false,
		tooltipOpts: {
			defaultTheme: false
		}
	}


	var plot = $.plot("#demo-realtime-chart", [ getRandomData() ], flotOptions);
	function update() {
		plot.setData([getRandomData()]);

		// Since the axes don't change, we don't need to call plot.setupGrid()

		plot.draw();
		setTimeout(update, updateInterval);
	}
	update();










	// GAUGE PLUGIN
	// =================================================================
	// Require Gauge.js
	// -----------------------------------------------------------------
	// http://bernii.github.io/gauge.js/
	// =================================================================
	var opts = {
		lines: 10, // The number of lines to draw
		angle: 0, // The length of each line
		lineWidth: 0.41, // The line thickness
		pointer: {
			length: 0.75, // The radius of the inner circle
			strokeWidth: 0.035, // The rotation offset
			color: '#769f48' // Fill color
		},
		limitMax: 'true', // If true, the pointer will not go past the end of the gauge
		colorStart: '#fff', // Colors
		colorStop: '#fff', // just experiment with them
		strokeColor: '#8ab75a', // to see which ones work best for you
		generateGradient: true
	};


	var target = document.getElementById('demo-gauge'); // your canvas element
	var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
	gauge.maxValue = 100; // set max gauge value
	gauge.animationSpeed = 32; // set animation speed (32 is default value)
	gauge.set(57); // set actual value
	gauge.setTextField(document.getElementById("demo-gauge-text"));












	// PIE CHART
	// =================================================================
	// Require easyPieChart
	// -----------------------------------------------------------------
	// http://rendro.github.io/easy-pie-chart/
	// =================================================================
	$('#demo-pie-1').easyPieChart({
		barColor :'#ffffff',
		scaleColor:'#8b5284',
		trackColor : '#8b5284',
		lineCap : 'round',
		lineWidth :8,
		onStep: function(from, to, percent) {
			$(this.el).find('.pie-value').text(Math.round(percent) + '%');
		}
	});









	// MEDIUM WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================

	// on Android, a nasty hack is needed: {"resizeClear": true}
	skyconsOptions = {
		"color": "#fff",
		"resizeClear": true
	}

	/* Main Icon */
	var skycons = new Skycons(skyconsOptions);
	skycons.add("demo-weather-md-icon-1", Skycons.PARTLY_CLOUDY_DAY);
	skycons.play();



	/* Small Icons*/
	var skycons2 = new Skycons(skyconsOptions);
	skycons2.add("demo-weather-md-icon-2", Skycons.CLOUDY);
	skycons2.play();


	var skycons3 = new Skycons(skyconsOptions);
	skycons3.add("demo-weather-md-icon-3", Skycons.WIND);
	skycons3.play();


	var skycons4 = new Skycons(skyconsOptions);
	skycons4.add("demo-weather-md-icon-4", Skycons.RAIN);
	skycons4.play();


	var skycons5 = new Skycons(skyconsOptions);
	skycons5.add("demo-weather-md-icon-5", Skycons.PARTLY_CLOUDY_DAY);
	skycons5.play();







	// LARGE WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================

	/* Main Icon */
	var skycons = new Skycons(skyconsOptions);
	skycons.add("demo-weather-lg-icon-1", Skycons.CLEAR_DAY);
	skycons.play();


	/* Small Icons*/
	var skycons2 = new Skycons(skyconsOptions);
	skycons2.add("demo-weather-lg-icon-2", Skycons.CLOUDY);
	skycons2.play();


	var skycons3 = new Skycons(skyconsOptions);
	skycons3.add("demo-weather-lg-icon-3", Skycons.WIND);
	skycons3.play();


	var skycons4 = new Skycons(skyconsOptions);
	skycons4.add("demo-weather-lg-icon-4", Skycons.RAIN);
	skycons4.play();


	var skycons5 = new Skycons(skyconsOptions);
	skycons5.add("demo-weather-lg-icon-5", Skycons.PARTLY_CLOUDY_DAY);
	skycons5.play();


	var skycons6 = new Skycons(skyconsOptions);
	skycons6.add("demo-weather-lg-icon-6", Skycons.WIND);
	skycons6.play();


	var skycons7 = new Skycons(skyconsOptions);
	skycons7.add("demo-weather-lg-icon-7", Skycons.CLOUDY);
	skycons7.play();











	// SMALL WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================

	var skycons = new Skycons(skyconsOptions);
	skycons.add("demo-weather-sm-icon", Skycons.RAIN);
	skycons.play();











	// EXTRA SMALL WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================
	skycons = new Skycons(skyconsOptions);
	skycons.add("demo-weather-xs-icon-1", Skycons.CLEAR_DAY);
	skycons.play();








	// EXTRA SMALL WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================

	skycons = new Skycons({
		"color": "#00b19d",
		"resizeClear": true
	});

	skycons.add("demo-weather-xs-icon-2", Skycons.PARTLY_CLOUDY_DAY);
	skycons.play();


});
