
// Form-Wizard.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).ready(function() {



	// FORM WIZARD
	// =================================================================
	// Require Bootstrap Wizard
	// http://vadimg.com/twitter-bootstrap-wizard-example/
	// =================================================================


	// MAIN FORM WIZARD
	// =================================================================
	$('#demo-main-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
			return false;
		},
		onInit : function(){
			$('#demo-main-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
			var $total = navigation.find('li').length;
			var $current = index+1;
			var $percent = ($current/$total) * 100;
			var wdt = 100/$total;
			var lft = wdt*index;

			$('#demo-main-wz').find('.progress-bar').css({width:wdt+'%',left:lft+"%", 'position':'relative', 'transition':'all .5s'});


			// If it's the last tab then hide the last button and show the finish instead
			if($current >= $total) {
				$('#demo-main-wz').find('.next').hide();
				$('#demo-main-wz').find('.finish').show();
				$('#demo-main-wz').find('.finish').prop('disabled', false);
			} else {
				$('#demo-main-wz').find('.next').show();
				$('#demo-main-wz').find('.finish').hide().prop('disabled', true);
			}
		}
	});




	// CLASSIC FORM WIZARD
	// =================================================================
	$('#demo-cls-wz').bootstrapWizard({
		tabClass		: 'wz-classic',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
			return false;
		},
		onInit : function(){
			$('#demo-cls-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
			var $total = navigation.find('li').length;
			var $current = index+1;
			var $percent = ($current/$total) * 100;
			var wdt = 100/$total;
			var lft = wdt*index;
			$('#demo-cls-wz').find('.progress-bar').css({width:$percent+'%'});

			// If it's the last tab then hide the last button and show the finish instead
			if($current >= $total) {
				$('#demo-cls-wz').find('.next').hide();
				$('#demo-cls-wz').find('.finish').show();
				$('#demo-cls-wz').find('.finish').prop('disabled', false);
			} else {
				$('#demo-cls-wz').find('.next').show();
				$('#demo-cls-wz').find('.finish').hide().prop('disabled', true);
			}
		}
	});




	// CIRCULAR FORM WIZARD
	// =================================================================
	$('#demo-step-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
			return false;
		},
		onInit : function(){
			$('#demo-step-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
			var $total = navigation.find('li').length;
			var $current = index+1;
			var $percent = (index/$total) * 100;
			var wdt = 100/$total;
			var lft = wdt*index;
			var margin = (100/$total)/2;
			$('#demo-step-wz').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});


			// If it's the last tab then hide the last button and show the finish instead
			if($current >= $total) {
				$('#demo-step-wz').find('.next').hide();
				$('#demo-step-wz').find('.finish').show();
				$('#demo-step-wz').find('.finish').prop('disabled', false);
			} else {
				$('#demo-step-wz').find('.next').show();
				$('#demo-step-wz').find('.finish').hide().prop('disabled', true);
			}
		}
	});



	// CIRCULAR FORM WIZARD
	// =================================================================
	$('#demo-cir-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
		return false;
		},
		onInit : function(){
		$('#demo-cir-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
		var $total = navigation.find('li').length;
		var $current = index+1;
		var $percent = (index/$total) * 100;
		var margin = (100/$total)/2;
		$('#demo-cir-wz').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});

		navigation.find('li:eq('+index+') a').trigger('focus');


		// If it's the last tab then hide the last button and show the finish instead
		if($current >= $total) {
			$('#demo-cir-wz').find('.next').hide();
			$('#demo-cir-wz').find('.finish').show();
			$('#demo-cir-wz').find('.finish').prop('disabled', false);
		} else {
			$('#demo-cir-wz').find('.next').show();
			$('#demo-cir-wz').find('.finish').hide().prop('disabled', true);
		}
		}
	})




	// FORM WIZARD WITH VALIDATION
	// =================================================================
	$('#demo-bv-wz').bootstrapWizard({
		tabClass		: 'wz-steps',
		nextSelector	: '.next',
		previousSelector	: '.previous',
		onTabClick: function(tab, navigation, index) {
			return false;
		},
		onInit : function(){
			$('#demo-bv-wz').find('.finish').hide().prop('disabled', true);
		},
		onTabShow: function(tab, navigation, index) {
			var $total = navigation.find('li').length;
			var $current = index+1;
			var $percent = (index/$total) * 100;
			var margin = (100/$total)/2;
			$('#demo-bv-wz').find('.progress-bar').css({width:$percent+'%', 'margin': 0 + 'px ' + margin + '%'});

			navigation.find('li:eq('+index+') a').trigger('focus');


			// If it's the last tab then hide the last button and show the finish instead
			if($current >= $total) {
				$('#demo-bv-wz').find('.next').hide();
				$('#demo-bv-wz').find('.finish').show();
				$('#demo-bv-wz').find('.finish').prop('disabled', false);
			} else {
				$('#demo-bv-wz').find('.next').show();
				$('#demo-bv-wz').find('.finish').hide().prop('disabled', true);
			}
		},
		onNext: function(){
			isValid = null;
			$('#demo-bv-wz-form').bootstrapValidator('validate');


			if(isValid === false)return false;
		}
	});




	// FORM VALIDATION
	// =================================================================
	// Require Bootstrap Validator
	// http://bootstrapvalidator.com/
	// =================================================================



});
