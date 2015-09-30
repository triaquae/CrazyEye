
// Charts.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



 $(document).ready(function() {



	// GAUGE JS
	// =================================================================
	// Require GaugeJS
	// -----------------------------------------------------------------
	// http://bernii.github.io/gauge.js/
	// =================================================================
	var opts = {
		lines: 10, // The number of lines to draw
		angle: 0, // The length of each line
		lineWidth: 0.3, // The line thickness
		pointer: {
			length: 0.45, // The radius of the inner circle
			strokeWidth: 0.035, // The rotation offset
			color: '#242d3c' // Fill color
		},
		limitMax: 'true', // If true, the pointer will not go past the end of the gauge
		colorStart: '#177bbb', // Colors
		colorStop: '#177bbb', // just experiment with them
		strokeColor: '#ddd', // to see which ones work best for you
		generateGradient: true
	};


	var target = document.getElementById('demo-gauge'); // your canvas element
	var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
	gauge.maxValue = 1500; // set max gauge value
	gauge.animationSpeed = 32; // set animation speed (32 is default value)
	gauge.set(570); // set actual value
	gauge.setTextField(document.getElementById("demo-gauge-txt"));



	// REALTIME SAMPLE
	// =================================================================
	var updateGauge;
	var gaugeSwitch = document.getElementById('demo-auto-gauge');
	gaugeSwitch.checked = false;
	new Switchery(gaugeSwitch);

	gaugeSwitch.onchange = function(){
		if (gaugeSwitch.checked) {
			updateGauge = setInterval(function(){
				gauge.set(nifty.randomInt(1,1500));
			},2000)
		}else{
			clearInterval(updateGauge);
		}
	};







	// EASY PIE CHART
	// =================================================================
	// Require easyPieChart
	// -----------------------------------------------------------------
	// http://rendro.github.io/easy-pie-chart/
	// =================================================================
	$('#demo-pie-1').easyPieChart({
		barColor :'#68b828',
		scaleColor: false,
		trackColor : '#eee',
		lineCap : 'round',
		lineWidth :8,
		onStep: function(from, to, percent) {
			$(this.el).find('.pie-value').text(Math.round(percent) + '%');
		}
	});
	$('#demo-pie-2').easyPieChart({
		barColor :'#8465d4',
		scaleColor:false,
		trackColor : '#eee',
		lineCap : 'butt',
		lineWidth :8,
		onStep: function(from, to, percent) {
			$(this.el).find('.pie-value').text(Math.round(percent) + '%');
		}
	});




	// SPARKLINE AREA CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-area").sparkline([57,69,70,68,73,76,75,79,73,76,77,73], {
		type: 'line',
		width: '130',
		height: '75',
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



	// SPARKLINE LINE CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-line").sparkline([345,404,305,455,378,767], {
		type: 'line',
		width: '130',
		height: '75',
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


	// SPARKLINE BAR CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-bar").sparkline([40,32,53,45,67,45,56,34,67,76], {
		type: 'bar',
		height: '75',
		barWidth: 9,
		barSpacing: 3,
		zeroAxis: false,
		tooltipChartTitle: 'Daily Sales',
		tooltipSuffix:' Sales',
		barColor: '#fff'}
	);


	// SPARKLINE PIE CHART
	// =================================================================
	// Require sparkline
	// -----------------------------------------------------------------
	// http://omnipotent.net/jquery.sparkline/#s-about
	// =================================================================
	$("#demo-sparkline-pie").sparkline([5, 12, 17 ,55], {
		type: 'pie',
		width: '75',
		height: '75',
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



	// MORRIS AREA CHART
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================

	Morris.Area({
		element: 'demo-morris-area',
		data: [{
			period: 'January',
			dl: 77,
			up: 25
			}, {
			period: 'February',
			dl: 127,
			up: 58
			}, {
			period: 'March',
			dl: 115,
			up: 46
			}, {
			period: 'April',
			dl: 239,
			up: 57
			}, {
			period: 'May',
			dl: 46,
			up: 75
			}, {
			period: 'June',
			dl: 97,
			up: 57
			}, {
			period: 'July',
			dl: 105,
			up: 70
			}, {
			period: 'August',
			dl: 115,
			up: 106
			}, {
			period: 'September',
			dl: 239,
			up: 187
			}, {
			period: 'October',
			dl: 246,
			up: 215
			}],
		gridEnabled: false,
		gridLineColor: 'transparent',
		behaveLikeLine: true,
		xkey: 'period',
		ykeys: ['dl', 'up'],
		labels: ['Visitor', 'Pageview'],
		lineColors: ['#045d97'],
		pointSize: 0,
		pointStrokeColors : ['#045d97'],
		lineWidth: 0,
		resize:true,
		hideHover: 'auto',
		fillOpacity: 0.7,
		parseTime:false
	});


	// MORRIS LINE CHART
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================
	var day_data = [
		{"elapsed": "I", "value": 34},
		{"elapsed": "II", "value": 24},
		{"elapsed": "III", "value": 3},
		{"elapsed": "IV", "value": 12},
		{"elapsed": "V", "value": 13},
		{"elapsed": "VI", "value": 22},
		{"elapsed": "VII", "value": 5},
		{"elapsed": "VIII", "value": 26},
		{"elapsed": "IX", "value": 12},
		{"elapsed": "X", "value": 19}
	];
	Morris.Line({
		element: 'demo-morris-line',
		data: day_data,
		xkey: 'elapsed',
		ykeys: ['value'],
		labels: ['value'],
		gridEnabled: false,
		gridLineColor: 'transparent',
		lineColors: ['#045d97'],
		lineWidth: 2,
		parseTime: false,
		resize:true,
		hideHover: 'auto'
	});



	// MORRIS BAR CHART
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================
	Morris.Bar({
		element: 'demo-morris-bar',
		data: [
			{ y: '1', a: 100, b: 90 },
			{ y: '2', a: 75,  b: 65 },
			{ y: '3', a: 20,  b: 15 },
			{ y: '5', a: 50,  b: 40 },
			{ y: '6', a: 75,  b: 95 },
			{ y: '7', a: 15,  b: 65 },
			{ y: '8', a: 70,  b: 100 },
			{ y: '9', a: 100, b: 70 },
			{ y: '10', a: 50, b: 70 },
			{ y: '11', a: 20, b: 10 },
			{ y: '12', a: 40, b: 90 },
			{ y: '13', a: 70, b: 30 },
			{ y: '14', a: 50, b: 50 },
			{ y: '15', a: 100, b: 90 }
		],
		xkey: 'y',
		ykeys: ['a', 'b'],
		labels: ['Series A', 'Series B'],
		gridEnabled: false,
		gridLineColor: 'transparent',
		barColors: ['#177bbb', '#afd2f0'],
		resize:true,
		hideHover: 'auto'
	});



	// MORRIS DONUT CHART
	// =================================================================
	// Require MorrisJS Chart
	// -----------------------------------------------------------------
	// http://morrisjs.github.io/morris.js/
	// =================================================================
	Morris.Donut({
		element: 'demo-morris-donut',
		data: [
			{label: "Download Sales", value: 12},
			{label: "In-Store Sales", value: 30},
			{label: "Mail-Order Sales", value: 20}
		],
		colors: [
			'#a6c600',
			'#177bbb',
			'#afd2f0'
		],
		resize:true
	});



	// FLOT CHART
	// =================================================================
	// Require Flot Charts
	// -----------------------------------------------------------------
	// http://www.flotcharts.org/
	// =================================================================

	var pageviews = [[1, 1700], [2, 1200], [3, 1090], [4, 1550], [5, 1700], [6, 1850], [7, 2736], [8, 3045], [9, 3779], [10, 4895], [11, 5209], [12, 5100]],
	visitor = [[1, 456], [2, 589], [3, 354], [4, 558], [5, 254], [6, 656], [7, 124], [8, 523], [9, 256], [10, 987], [11, 854], [12, 965]];

	var plot = $.plot("#demo-flot-line", [
			{
				label: 'Pageviews',
				data: pageviews,
				lines: {
					show: true,
					lineWidth:2,
					fill: true,
					fillColor: {
						colors: [{opacity: 0.5}, {opacity: 0.5}]
					}
				},
				points: {
					show: true,
					radius: 4
				}
			},
			{
				label: 'Visitors',
				data: visitor,
				lines: {
					show: true,
					lineWidth:2,
					fill: true,
					fillColor: {
						colors: [{opacity: 0.5}, {opacity: 0.5}]
					}
				},
				points: {
					show: true,
					radius: 4
				}
			}
		],{
		series: {
			lines: {
				show: true
			},
			points: {
				show: true
			},
			shadowSize: 0	// Drawing is faster without shadows
		},
		colors: ['#177bbb', '#177bbb'],
		legend: {
			show: true,
			position: 'nw',
			margin: [15, 0]
		},
		grid: {
			borderWidth: 0,
			hoverable: true,
			clickable: true
		},
		yaxis: {
			ticks: 4, tickColor: '#eeeeee'
		},
		xaxis: {
			ticks: 12,
			tickColor: '#ffffff'
		}
	});


	// Flot tooltip
	// =================================================================
	$("<div id='demo-flot-tooltip'></div>").css({
		position: "absolute",
		display: "none",
		padding: "10px",
		color: "#fff",
		"text-align":"right",
		"background-color": "#1c1e21"
	}).appendTo("body");


	$("#demo-flot-line").bind("plothover", function (event, pos, item) {

		if (item) {
			var x = item.datapoint[0].toFixed(2),  y = item.datapoint[1];
			$("#demo-flot-tooltip").html("<p class='h4'>" + item.series.label + "</p>" + y)
				.css({top: item.pageY+5, left: item.pageX+5})
				.fadeIn(200);
		} else {
			$("#demo-flot-tooltip").hide();
		}

	});




	// FLOT PIE CHART
	// =================================================================
	// Require Flot Charts
	// -----------------------------------------------------------------
	// http://www.flotcharts.org/
	// =================================================================
	var dataSet = [
		{ label: "Comedy", data: 4119630000, color: "#177bbb" },
		{ label: "Action", data: 1012960000, color: "#a6c600" },
		{ label: "Adventure", data: 727080000, color: "#8669CC" },
		{ label: "Drama", data: 344120000, color: "#f84f9a" }
	];

	$.plot('#demo-flot-donut', dataSet, {
		series: {
			pie: {
				show: true,
				combine: {
				color: '#999',
				threshold: 0.1
				}
			}
		},
		legend: {
		show: false
		}
	});

});
