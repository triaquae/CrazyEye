/*! jquery.cookie v1.4.1 | MIT */
!function(a){"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof exports?a(require("jquery")):a(jQuery)}(function(a){function b(a){return h.raw?a:encodeURIComponent(a)}function c(a){return h.raw?a:decodeURIComponent(a)}function d(a){return b(h.json?JSON.stringify(a):String(a))}function e(a){0===a.indexOf('"')&&(a=a.slice(1,-1).replace(/\\"/g,'"').replace(/\\\\/g,"\\"));try{return a=decodeURIComponent(a.replace(g," ")),h.json?JSON.parse(a):a}catch(b){}}function f(b,c){var d=h.raw?b:e(b);return a.isFunction(c)?c(d):d}var g=/\+/g,h=a.cookie=function(e,g,i){if(void 0!==g&&!a.isFunction(g)){if(i=a.extend({},h.defaults,i),"number"==typeof i.expires){var j=i.expires,k=i.expires=new Date;k.setTime(+k+864e5*j)}return document.cookie=[b(e),"=",d(g),i.expires?"; expires="+i.expires.toUTCString():"",i.path?"; path="+i.path:"",i.domain?"; domain="+i.domain:"",i.secure?"; secure":""].join("")}for(var l=e?void 0:{},m=document.cookie?document.cookie.split("; "):[],n=0,o=m.length;o>n;n++){var p=m[n].split("="),q=c(p.shift()),r=p.join("=");if(e&&e===q){l=f(r,g);break}e||void 0===(r=f(r))||(l[q]=r)}return l};h.defaults={},a.removeCookie=function(b,c){return void 0===a.cookie(b)?!1:(a.cookie(b,"",a.extend({},c,{expires:-1})),!a.cookie(b))}});



// Nifty-demo.js
// ====================================================================
// Set user options for current page.
// This file is only used for demonstration purposes.
// ====================================================================
// - ThemeOn.net -


$(document).ready(function () {

	// SETTINGS WINDOW
	// =================================================================

	var demoSetBody = $('#demo-set');
	var demoSetIcon = $('#demo-set-icon');
	var demoSetBtnGo = $('#demo-set-btngo');

	if (demoSetBody.length) {
		$('html').on('click', function (e) {
			if (demoSetBody.hasClass('open')) {
				if (!$(e.target).closest('#demo-set').length) {
					demoSetBody.removeClass('open');
				}
			}
		});
		$('#demo-set-btn').on('click', function (e) {
			e.stopPropagation();
			demoSetBody.toggleClass('open');
		});

		function are_cookies_enabled() {
			var cookieEnabled = (navigator.cookieEnabled) ? true : false;
			if (typeof navigator.cookieEnabled == "undefined" && !cookieEnabled) {
				document.cookie = "testcookie";
				cookieEnabled = (document.cookie.indexOf("testcookie") != -1) ? true : false;
			}
			return (cookieEnabled);
		}

		if (are_cookies_enabled() == false) {
			$.niftyNoty({
				type: 'danger',
				message: "Your browser's <strong>cookie</strong> functionality is turned off. Some settings won\'t work as expected....",
				container: '#demo-set-alert',
				closeBtn: false
			});

			$('#demo-set').addClass('no-cookie');
		}

	};






	// TRANSITION EFFECTS
	// =================================================================
	// =================================================================
	var effectList = 'easeInQuart easeOutQuart easeInBack easeOutBack easeInOutBack steps jumping rubber',
		animCheckbox = $('#demo-anim'),
		transitionVal = $('#demo-ease');

	// Animations checkbox
	animCheckbox.on('change', function () {
		if (animCheckbox.niftyCheck('isChecked')) {
			nifty.container.addClass('effect');
			transitionVal.prop('disabled', false).selectpicker('refresh');
			setCookie('settings-animation', 'effect');
		} else {
			nifty.container.removeClass('effect ' + effectList);
			transitionVal.prop('disabled', true).selectpicker('refresh');
			setCookie('settings-animation', 'none');
		}
	});


	// Transition selectbox
	transitionVal.selectpicker().on('change', function (e) {
		var optionSelected = $("option:selected", this);
		var valueSelected = this.value;

		if (valueSelected) {
			nifty.container.removeClass(effectList).addClass(valueSelected);
			setCookie('settings-animation', valueSelected);
		}
	});









	// NAVIGATION
	// =================================================================
	// =================================================================
	var collapsedCheckbox = $('#demo-nav-coll');
	var navFixedCheckbox = $('#demo-nav-fixed');
	var navOffcanvasSB = $('#demo-nav-offcanvas');


	// Collapsing/Expanding Navigation
	// =================================================================
	collapsedCheckbox.on('change', function () {
		if ($.cookie('settings-nav-offcanvas')) {
			setCookie('settings-nav-offcanvas', false);
			setCookie('settings-nav-collapsed', true);
			demoSetBody.removeClass('open');
			location.reload(true);
			return false;
		}


		//$.niftyNav('colExpToggle');
		// $.niftyNav('colExpToggle', function(){...Callback..});



		if (collapsedCheckbox.niftyCheck('isChecked')) {
			$.niftyNav('collapse');
			setCookie('settings-nav-collapsed', true);
		} else {
			$.niftyNav('expand');
			setCookie('settings-nav-collapsed', false);
		}
	});





	// Fixed Position
	// =================================================================
	navFixedCheckbox.on('change', function () {
		if (navFixedCheckbox.niftyCheck('isChecked')) {
			$.niftyNav('fixedPosition');
			setCookie('settings-nav-fixed', true);
		} else {
			$.niftyNav('staticPosition');
			setCookie('settings-nav-fixed', false);
		}
	});





	// Offcanvas Navigation
	// =================================================================
	navOffcanvasSB.selectpicker().on('change', function () {
		setCookie('settings-nav-collapsed', false)
		setCookie('settings-nav-offcanvas', this.value);
		demoSetBody.removeClass('open');
		location.reload(true);
	}).selectpicker('val', $.cookie('settings-nav-offcanvas'));











	// ASIDE
	// =================================================================
	// =================================================================
	var asdVisCheckbox = $('#demo-asd-vis');
	var asdFixedCheckbox = $('#demo-asd-fixed');
	var asdPosCheckbox = $('#demo-asd-align');
	var asdThemeCheckbox = $('#demo-asd-themes');


	// Visible
	// =================================================================
	asdVisCheckbox.on('change', function () {
		if (asdVisCheckbox.niftyCheck('isChecked')) {
			$.niftyAside('show');
			setCookie('settings-asd-visibility', true);
		} else {
			$.niftyAside('hide');
			setCookie('settings-asd-visibility', false);
		}
	});







	// Fixed Position
	// =================================================================
	asdFixedCheckbox.on('change', function () {
		if (asdFixedCheckbox.niftyCheck('isChecked')) {
			$.niftyAside('fixedPosition');
			setCookie('settings-asd-fixed', true);
		} else {
			$.niftyAside('staticPosition');
			setCookie('settings-asd-fixed', false);
		};
	});






	// Position
	// =================================================================
	asdPosCheckbox.on('change', function () {
		if (asdPosCheckbox.niftyCheck('isChecked')) {
			$.niftyAside('alignLeft');
			setCookie('settings-asd-align', 'left');
		} else {
			$.niftyAside('alignRight');
			setCookie('settings-asd-align', 'right');
		};
	});







	// Color Themes
	// =================================================================
	asdThemeCheckbox.on('change', function () {
		if (asdThemeCheckbox.niftyCheck('isChecked')) {
			$.niftyAside('brightTheme');
			setCookie('settings-asd-theme', 'bright');
		} else {
			$.niftyAside('darkTheme');
			setCookie('settings-asd-theme', 'dark');
		};
	});









	// NAVBAR
	// =================================================================
	// =================================================================
	var navbarFixedCheckbox = $('#demo-navbar-fixed');

	// Fixed Position
	// =================================================================
	navbarFixedCheckbox.on('change', function () {
		if (navbarFixedCheckbox.niftyCheck('isChecked')) {
			nifty.container.addClass('navbar-fixed');
			setCookie('settings-navbar-fixed', true);
		} else {
			nifty.container.removeClass('navbar-fixed');
			setCookie('settings-navbar-fixed', false);
		}

		// Refresh the aside, to enable or disable the "Bootstrap Affix" when the navbar is in a "static position".
		nifty.mainNav.niftyAffix('update');
		nifty.aside.niftyAffix('update');
	});









	// FOOTER
	// =================================================================
	// =================================================================
	var footerFixedCheckbox = $('#demo-footer-fixed');

	// Fixed Position
	// =================================================================
	footerFixedCheckbox.on('change', function () {
		if (footerFixedCheckbox.niftyCheck('isChecked')) {
			nifty.container.addClass('footer-fixed');
			setCookie('settings-footer-fixed', true);
		} else {
			nifty.container.removeClass('footer-fixed');
			setCookie('settings-footer-fixed', false);
		}
	});









	// COLOR THEMES
	// =================================================================
	var themeBtn = $('.demo-theme'),
		changeTheme = function (themeName, type) {
			var themeCSS = $('#theme'),
				filename = 'css/themes/type-' + type + '/' + themeName + '.min.css';

			if (themeCSS.length) {
				themeCSS.prop('href', filename);
			} else {
				themeCSS = '<link id="theme" href="' + filename + '" rel="stylesheet">';
				$('head').append(themeCSS);
			}
			setCookie('settings-theme-name', themeName);
			setCookie('settings-theme-type', type);
		};


	$('#demo-theme').on('click', '.demo-theme', function (e) {
		e.preventDefault();
		var el = $(this);
		if (el.hasClass('disabled')) {
			return false;
		}
		changeTheme(el.attr('data-theme'), el.attr('data-type'));
		themeBtn.removeClass('disabled');
		el.addClass('disabled');
		return false;
	});









	// LANGUAGE SWITCHER
	// =================================================================
	// Require Admin Core Javascript
	// http://www.themeOn.net
	// =================================================================
	$('#demo-lang-switch').niftyLanguage({
		onChange: function (e) {
			$.niftyNoty({
				type: 'info',
				icon: 'fa fa-info fa-lg',
				title: 'Language changed',
				message: 'The language apparently changed, the selected language is : <strong> ' + e.id + ' ' + e.name + '</strong> '
			});
		}
	});









	var elems = Array.prototype.slice.call(document.querySelectorAll('.demo-switch'));
	elems.forEach(function (html) {
		var switchery = new Switchery(html);
	});









	// GENERATE RANDOM ALERT
	// =================================================================
	// Require Admin Core Javascript
	// http://themeon.net
	// =================================================================

	var dataAlert = [{
			icon: 'fa fa-info fa-lg',
			title: "Info",
			type: "info"
	}, {
			icon: 'fa fa-star fa-lg',
			title: "Primary",
			type: "primary"
	}, {
			icon: 'fa fa-thumbs-up fa-lg',
			title: "Success",
			type: "success"
	}, {
			icon: 'fa fa-bolt fa-lg',
			title: "Warning",
			type: "warning"
	}, {
			icon: 'fa fa-times fa-lg',
			title: "Danger",
			type: "danger"
	}, {
			icon: 'fa fa-leaf fa-lg',
			title: "Mint",
			type: "mint"
	}, {
			icon: 'fa fa-shopping-cart fa-lg',
			title: "Purple",
			type: "purple"
	}, {
			icon: 'fa fa-heart fa-lg',
			title: "Pink",
			type: "pink"
	}, {
			icon: 'fa fa-sun-o fa-lg',
			title: "Dark",
			type: "dark"
	}
	];



	// GROWL LIKE NOTIFICATIONS
	// =================================================================
	// Require Admin Core Javascript
	// =================================================================
	$('#demo-alert').on('click', function (ev) {
		ev.preventDefault();
		var dataNum = nifty.randomInt(0, 8);


		$.niftyNoty({
			type: dataAlert[dataNum].type,
			icon: dataAlert[dataNum].icon,
			title: dataAlert[dataNum].title,
			message: "Lorem ipsum dolor sit amet.",
			container: 'floating',
			timer: 3500
		});
	});






	// ALERT ON TOP PAGE
	// =================================================================
	// Require Admin Core Javascript
	// =================================================================

	// Show random page alerts.
	$('#demo-page-alert').on('click', function (ev) {
		ev.preventDefault();

		var dataNum = nifty.randomInt(0, 8),
			timer = function () {
				if (nifty.randomInt(0, 5) < 4) return 3000
				return 0;
			}();



		// Show random page alerts.
		$.niftyNoty({
			type: dataAlert[dataNum].type,
			icon: dataAlert[dataNum].icon,
			title: function () {
				if (timer > 0) {
					return 'Autoclose Alert'
				}
				return 'Sticky Alert Box'
			}(),
			message: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.',
			timer: timer
		});
	});






	// ASIDE
	// =================================================================
	// Toggle Visibe
	// =================================================================
	$('#demo-toggle-aside').on('click', function (ev) {
		ev.preventDefault();
		if (!nifty.container.hasClass('aside-in')) {
			$.niftyAside('show');
			asdVisCheckbox.niftyCheck('toggleOn')
		} else {
			$.niftyAside('hide');
			asdVisCheckbox.niftyCheck('toggleOff')
		}
	});









	// INIT - Check and apply all settings are available.
	// =================================================================

	if (typeof window.demoLayout !== 'undefined') return;


	var cookieList = [
		'settings-animation',
		'settings-nav-fixed',
		'settings-nav-collapsed',
		'settings-nav-offcanvas',
		'settings-asd-visibility',
		'settings-asd-fixed',
		'settings-asd-align',
		'settings-asd-theme',
		'settings-navbar-fixed',
		'settings-footer-fixed',
		'settings-theme-type',
		'settings-theme-name'
	],
		setCookie = function (name, value) {
			if (value == false) {
				$.removeCookie(name, {
					path: '/'
				});
			} else {
				$.cookie(name, ((value === true) ? '1' : value), {
					expires: 7,
					path: '/'
				});
			}
		},
		removeAllCookie = function () {
			for (var i = 0; i < cookieList.length; i++) {
				$.removeCookie(cookieList[i], {
					path: '/'
				});
			}
		};


	// Reser all settings
	$('#demo-reset-settings').on('click', function () {
		animCheckbox.niftyCheck('toggleOn');
		nifty.container.removeClass(effectList).addClass('effect');
		transitionVal.selectpicker('val', 'effect');


		navFixedCheckbox.niftyCheck('toggleOff');
		$.niftyNav('staticPosition');

		collapsedCheckbox.niftyCheck('toggleOff');
		$.niftyNav('expand');

		nifty.container.removeClass('mainnav-in mainnav-out mainnav-sm');
		navOffcanvasSB.selectpicker('val', 'none');


		asdVisCheckbox.niftyCheck('toggleOff');
		$.niftyAside('hide');


		asdFixedCheckbox.niftyCheck('toggleOff');
		$.niftyAside('staticPosition');

		asdPosCheckbox.niftyCheck('toggleOff');
		$.niftyAside('alignRight');


		asdThemeCheckbox.niftyCheck('toggleOff');
		$.niftyAside('darkTheme');


		navbarFixedCheckbox.niftyCheck('toggleOff');
		nifty.container.removeClass('navbar-fixed');
		nifty.mainNav.niftyAffix('update');
		nifty.aside.niftyAffix('update');

		footerFixedCheckbox.niftyCheck('toggleOff');
		nifty.container.removeClass('footer-fixed');


		//changeTheme('theme-navy', 'mainnav');
		$('#theme').remove();

		$('.demo-theme').removeClass('disabled').filter('[data-type="mainnav"]').filter('[data-theme="theme-navy"]').addClass('disabled');

		removeAllCookie();

		$.niftyNoty({
			icon: 'fa fa-check fa-lg',
			type: 'success',
			message: "All settings has been restored to the factory default values.",
			container: '#demo-set-alert',
			timer: 4000
		});


	});



	// Animation cookie
	if ($.cookie('settings-animation')) {
		if ($.cookie('settings-animation') == 'none') {
			nifty.container.removeClass('effect ' + effectList);
			animCheckbox.niftyCheck('toggleOff');
			transitionVal.prop('disabled', true).selectpicker('refresh');
		} else {
			animCheckbox.niftyCheck('toggleOn');
			nifty.container.addClass('effect ' + $.cookie('settings-animation'));
			transitionVal.selectpicker('val', $.cookie('settings-animation'))
		}
	}




	// Fixed navigation
	if ($.cookie('settings-nav-fixed') == 1 || nifty.container.hasClass('mainnav-fixed')) {
		navFixedCheckbox.niftyCheck('toggleOn');
		$.niftyNav('fixedPosition');
	} else {
		navFixedCheckbox.niftyCheck('toggleOff');
		$.niftyNav('staticPosition');
	};





	// Collapsed navigation
	if ($.cookie('settings-nav-collapsed') == 1) {
		collapsedCheckbox.niftyCheck('toggleOn');
		$.niftyNav('collapse');
		$('.mainnav-toggle').removeClass('push slide reveal')
	} else {
		collapsedCheckbox.niftyCheck('toggleOff');
		if ($.cookie('settings-nav-offcanvas')) {
			nifty.container.removeClass('mainnav-in mainnav-sm mainnav-lg');
			$.niftyNav($.cookie('settings-nav-offcanvas') + 'Out');
			$('.mainnav-toggle').removeClass('push slide reveal').addClass($.cookie('settings-nav-offcanvas'));
		}
	};



	if (nifty.container.hasClass('aside-in')) {
		asdVisCheckbox.niftyCheck('toggleOn');
	} else {
		asdVisCheckbox.niftyCheck('toggleOff');
	}



	if (nifty.container.hasClass('aside-fixed')) {
		asdFixedCheckbox.niftyCheck('toggleOn');
	} else {
		asdFixedCheckbox.niftyCheck('toggleOff');
	}


	if (nifty.container.hasClass('aside-left')) {
		asdPosCheckbox.niftyCheck('toggleOn');
	} else {
		asdPosCheckbox.niftyCheck('toggleOff');
	}


	if (nifty.container.hasClass('aside-left')) {
		asdThemeCheckbox.niftyCheck('toggleOn');
	} else {
		asdThemeCheckbox.niftyCheck('toggleOff');
	}





	// Fixed navbar
	if ($.cookie('settings-navbar-fixed') == 1 || nifty.container.hasClass('navbar-fixed')) {
		navbarFixedCheckbox.niftyCheck('toggleOn');
		nifty.container.addClass('navbar-fixed');

		// Refresh the aside, to enable or disable the "Bootstrap Affix" when the navbar is in a "static position".
		nifty.mainNav.niftyAffix('update');
		nifty.aside.niftyAffix('update');
	} else {
		navbarFixedCheckbox.niftyCheck('toggleOff');
		nifty.container.removeClass('navbar-fixed');

		// Refresh the aside, to enable or disable the "Bootstrap Affix" when the navbar is in a "static position".
		nifty.mainNav.niftyAffix('update');
		nifty.aside.niftyAffix('update');
	};





	// Fixed footer
	if ($.cookie('settings-footer-fixed') == 1 || nifty.container.hasClass('footer-fixed')) {
		footerFixedCheckbox.niftyCheck('toggleOn');
		nifty.container.addClass('footer-fixed');
	} else {
		footerFixedCheckbox.niftyCheck('toggleOff');
		nifty.container.removeClass('footer-fixed');
	}




	// Themes
	if ($.cookie('settings-theme-name') && $.cookie('settings-theme-type')) {
		changeTheme($.cookie('settings-theme-name'), $.cookie('settings-theme-type'));

		$('.demo-theme').filter('[data-type=' + $.cookie('settings-theme-type') + ']').filter('[data-theme=' + $.cookie('settings-theme-name') + ']').addClass('disabled');
	} else {
		$('.demo-theme.demo-c-navy').addClass('disabled');
	}


});
