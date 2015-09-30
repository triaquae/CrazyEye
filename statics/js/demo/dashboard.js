
// Dashboard.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(window).on('load', function() {



	// Network chart ( Morris Line Chart )
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================

	var day_data = [
		{"elapsed": "2013 - 01", "value": 24, b:2},
		{"elapsed": "2013 - 02", "value": 34, b:22},
		{"elapsed": "2013 - 03", "value": 33, b:7},
		{"elapsed": "2013 - 04", "value": 22, b:6},
		{"elapsed": "2013 - 05", "value": 28, b:17},
		{"elapsed": "2013 - 06", "value": 60, b:15},
		{"elapsed": "2013 - 07", "value": 60, b:17},
		{"elapsed": "2013 - 08", "value": 70, b:7},
		{"elapsed": "2013 - 09", "value": 67, b:18},
		{"elapsed": "2013 - 10", "value": 86, b: 18},
		{"elapsed": "2013 - 11", "value": 86, b: 18},
		{"elapsed": "2013 - 12", "value": 113, b: 29},
		{"elapsed": "2014 - 01", "value": 130, b: 23},
		{"elapsed": "2014 - 02", "value": 114, b:10},
		{"elapsed": "2014 - 03", "value": 80, b:22},
		{"elapsed": "2014 - 04", "value": 109, b:7},
		{"elapsed": "2014 - 05", "value": 100, b:6},
		{"elapsed": "2014 - 06", "value": 105, b:17},
		{"elapsed": "2014 - 07", "value": 110, b:15},
		{"elapsed": "2014 - 08", "value": 102, b:17},
		{"elapsed": "2014 - 09", "value": 107, b:7},
		{"elapsed": "2014 - 10", "value": 60, b:18},
		{"elapsed": "2014 - 11", "value": 67, b: 18},
		{"elapsed": "2014 - 12", "value": 76, b: 18},
		{"elapsed": "2015 - 01", "value": 73, b: 29},
		{"elapsed": "2015 - 02", "value": 94, b: 13},
		{"elapsed": "2015 - 03", "value": 79, b: 24}
	];

	var chart = Morris.Area({
		element: 'morris-chart-network',
		data: day_data,
		axes:false,
		xkey: 'elapsed',
		ykeys: ['value', 'b'],
		labels: ['Download Speed', 'Upload Speed'],
		yLabelFormat :function (y) { return y.toString() + ' Mb/s'; },
		gridEnabled: false,
		gridLineColor: 'transparent',
		lineColors: ['#8eb5e3','#1b72bc'],
		lineWidth:0,
		pointSize:0,
		pointFillColors:['#3e80bd'],
		pointStrokeColors:'#3e80bd',
		fillOpacity:.7,
		gridTextColor:'#999',
		parseTime: false,
		resize:true,
		behaveLikeLine : true,
		hideHover: 'auto'
	});




	// Services chart ( Morris Donut Chart )
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================
	Morris.Donut({
		element: 'demo-morris-donut',
		data: [
			{label: "Supports", value: 12},
			{label: "Sales", value: 30},
			{label: "Comments", value: 20}
		],
		colors: [
			'#c686be',
			'#986291',
			'#ab6fa3'
		],
		resize:true
	});





	// Visitor chart ( Sparkline chart )
	// =================================================================
	// Require Sparkline Chart
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-chart-visitors").sparkline([476,643,356,453,745,976,867,886,984,645,767,799], {
		type: 'line',
		width: '110',
		height: '22',
		spotRadius: 3,
		lineWidth:1,
		lineColor:'rgba(255,255,255,.9)',
		fillColor: 'rgba(0,0,0,0.05)',
		spotColor: 'rgba(255,255,255,.5)',
		minSpotColor: 'rgba(255,255,255,.5)',
		maxSpotColor: 'rgba(255,255,255,.5)',
		highlightLineColor : '#ffffff',
		highlightSpotColor: '#ffffff',
		tooltipChartTitle: 'Visitors',
		tooltipSuffix:' k',
	});





	// Bounce rate chart ( Sparkline chart )
	// =================================================================
	// Require Sparkline Chart
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-chart-bounce-rate").sparkline([23,24,22,27,35,40,39,29,27,33,29,37], {
		type: 'line',
		width: '110',
		height: '22',
		spotRadius: 3,
		lineWidth:1,
		lineColor:'rgba(255,255,255,.9)',
		fillColor: 'rgba(0,0,0,0.05)',
		spotColor: 'rgba(255,255,255,.5)',
		minSpotColor: 'rgba(255,255,255,.5)',
		maxSpotColor: 'rgba(255,255,255,.5)',
		highlightLineColor : '#ffffff',
		highlightSpotColor: '#ffffff',
		tooltipChartTitle: 'Bounce rate',
		tooltipSuffix:' %'

	});






	// EXTRA SMALL WEATHER WIDGET
	// =================================================================
	// Require sckycons
	// -----------------------------------------------------------------
	// http://darkskyapp.github.io/skycons/
	// =================================================================

	// on Android, a nasty hack is needed: {"resizeClear": true}
	skyconsOptions = {
		"color": "#3bb5e8",
		"resizeClear": true
	}

	/* Main Icon */
	var skycons = new Skycons(skyconsOptions);
	skycons.add("demo-weather-xs-icon", Skycons.PARTLY_CLOUDY_DAY);
	skycons.play();






	// HDD USAGE - SPARKLINE LINE AREA CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-area").sparkline([57,69,70,68,73,76,75,79,73,76,77,73], {
		type: 'line',
		width: '110',
		height: '50',
		spotRadius: 2.5,
		lineWidth:1.5,
		lineColor:'rgba(255,255,255,.5)',
		fillColor: 'rgba(0,0,0,0.2)',
		spotColor: 'rgba(255,255,255,.5)',
		minSpotColor: 'rgba(255,255,255,.5)',
		maxSpotColor: 'rgba(255,255,255,.5)',
		highlightLineColor : '#ffffff',
		highlightSpotColor: '#ffffff',
		tooltipChartTitle: 'Usage',
		tooltipSuffix:' %'

	});







	// EARNING - SPARKLINE LINE CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-line").sparkline([345,404,305,455,378,767], {
		type: 'line',
		width: '110',
		height: '50',
		spotRadius: 2.5,
		lineWidth:1.5,
		lineColor:'#ffffff',
		fillColor: false,
		minSpotColor :false,
		maxSpotColor : false,
		highlightLineColor : '#ffffff',
		highlightSpotColor: '#ffffff',
		tooltipChartTitle: 'Earning',
		tooltipPrefix :'$ ',
		spotColor:'#ffffff',
		valueSpots : {
			'0:': '#ffffff'
		}
	});







	// SALES - SPARKLINE BAR CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-bar").sparkline([40,32,53,45,67,45,56,34,67,76], {
		type: 'bar',
		height: '50',
		barWidth: 7,
		barSpacing: 3,
		zeroAxis: false,
		tooltipChartTitle: 'Daily Sales',
		tooltipSuffix:' Sales',
		barColor: '#fff'}
	);






	// TOP MOVIE - SPARKLINE PIE CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-pie").sparkline([5, 12, 17 ,55], {
		type: 'pie',
		width: '50',
		height: '50',
		tooltipChartTitle: 'Top Movies',
		tooltipFormat: '{{offset:offset}} ({{percent.1}}%)',
		tooltipValueLookups: {
			'offset': {
				0: 'Drama',
				1: 'Action',
				2: 'Comedy',
				3: 'Adventure'
			}
		},
		sliceColors: ['#2d4859','#fe7211','#7ad689','#128376'],
	});









	// PANEL OVERLAY
	// =================================================================
	// Require Nifty js
	// -----------------------------------------------------------------
	// http://www.themeon.net
	// =================================================================
	$('#demo-panel-network-refresh').niftyOverlay().on('click', function(){
		var $el = $(this), relTime;

		$el.niftyOverlay('show');


		relTime = setInterval(function(){
			$el.niftyOverlay('hide');
			clearInterval(relTime);
		},2000);
	});








	// WEATHER WIDGET
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
	skycons.add("demo-weather-icon-1", Skycons.PARTLY_CLOUDY_DAY);
	skycons.play();



	/* Small Icons*/
	var skycons2 = new Skycons(skyconsOptions);
	skycons2.add("demo-weather-icon-2", Skycons.CLOUDY);
	skycons2.play();



	var skycons3 = new Skycons(skyconsOptions);
	skycons3.add("demo-weather-icon-3", Skycons.WIND);
	skycons3.play();



	var skycons4 = new Skycons(skyconsOptions);
	skycons4.add("demo-weather-icon-4", Skycons.RAIN);
	skycons4.play();



	var skycons5 = new Skycons(skyconsOptions);
	skycons5.add("demo-weather-icon-5", Skycons.PARTLY_CLOUDY_DAY);
	skycons5.play();



	// WELCOME NOTIFICATIONS
	// =================================================================
	// Require Admin Core Javascript
	// =================================================================
	 var fvisit  = setTimeout(function(){
		$.niftyNoty({
			type: 'dark',
			title: 'Hello Admin,',
			message: 'Lorem ipsum dolor sit amet consectetuer <br> adipiscing elit sed diam nonummy nibh.',
			container: 'floating',
			timer: 5500
		});
		clearTimeout(fvisit);
	 }, 3000);

});
