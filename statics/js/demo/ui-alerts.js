
// UI-Alerts.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).ready(function() {

	// [ DEMO ] GENERATE RANDOM ALERTS
	// =================================================================
	var dataAlert = [{
			type : "info"
		},{
			type : "primary"
		},{
			type : "success"
		},{
			type : "warning"
		},{
			type : "danger"
		},{
			type : "mint"
		},{
			type : "purple"
		},{
			type : "pink"
		},{
			type : "dark"
		}
	],
	alertContent = $('#demo-preview-alert-1').find('.alert').html(),
	autoClose = true;
	$('#demo-alert-close-1').on('nifty.ch.checked', function(){
		autoClose = true;
	});
	$('#demo-alert-close-2').on('nifty.ch.checked', function(){
		autoClose = false;
	});
	// =================================================================



	// PAGE ALERTS
	// =================================================================
	// Require Nifty Admin Javascript
	// http://www.themeon.net/
	// =================================================================
	$('#demo-alert-page').on('click', function(){
		dataNum = nifty.randomInt(0,8);
		contentHTML = alertContent.replace("btn-danger", "btn-"+dataAlert[dataNum].type);
		$.niftyNoty({
			type: dataAlert[dataNum].type,
			container : 'page',
			html : contentHTML,
			timer : autoClose ? 3000 : 0
		});
	});


	// PANEL ALERTS
	// =================================================================
	// Require Nifty Admin Javascript
	// http://www.themeon.net/
	// =================================================================
	$('#demo-alert-panel').on('click', function(){
		var dataNum = nifty.randomInt(0,8);
		var contentHTML = alertContent.replace("btn-danger", "btn-"+dataAlert[dataNum].type);

		$.niftyNoty({
			type: dataAlert[dataNum].type,
			container : '#demo-panel-alert',
			html : contentHTML,
			focus: false,
			timer : autoClose ? 3000 : 0
		});

		dataNum = nifty.randomInt(0,8);
		contentHTML = alertContent.replace("btn-danger", "btn-"+dataAlert[dataNum].type);

		$.niftyNoty({
			type: dataAlert[dataNum].type,
			container : '#demo-basic-panel-alert',
			html : contentHTML,
			focus: false,
			timer : autoClose ? 3000 : 0
		});
	});


	// GROW-LIKE / FLOATING ALERTS
	// =================================================================
	// Require Nifty Admin Javascript
	// http://www.themeon.net/
	// =================================================================
	$('#demo-alert-noty').on('click', function(){
		dataNum = nifty.randomInt(0,8);
		contentHTML = alertContent.replace("btn-danger", "btn-"+dataAlert[dataNum].type);

		$.niftyNoty({
			type: dataAlert[dataNum].type,
			container : 'floating',
			html : contentHTML,
			timer : autoClose ? 3000 : 0
		});
	});


	// [ DEMO ] ALERT SELECTOR
	// =================================================================
	var prevAlert = $('.demo-preview-alert');
	prevAlert.hide();
	$('#demo-preview-alert-1').fadeIn(300);
	$('#demo-alert-type-1').on('nifty.ch.checked', function(){
		prevAlert.hide();
		alertContent = $('#demo-preview-alert-1').find('.alert').html();
		$('#demo-preview-alert-1').fadeIn(300);
	}).niftyCheck('toggleOn');

	$('#demo-alert-type-2').on('nifty.ch.checked', function(){
		prevAlert.hide();
		alertContent = $('#demo-preview-alert-2').find('.alert').html();
		$('#demo-preview-alert-2').fadeIn(300);
	});

	$('#demo-alert-type-3').on('nifty.ch.checked', function(){
		prevAlert.hide();
		alertContent = $('#demo-preview-alert-3').find('.alert').html();
		$('#demo-preview-alert-3').fadeIn(300);
	});

	$('#demo-alert-type-4').on('nifty.ch.checked', function(){
		prevAlert.hide();
		alertContent = $('#demo-preview-alert-4').find('.alert').html();

		$('#demo-preview-alert-4').fadeIn(300);
	});
})
