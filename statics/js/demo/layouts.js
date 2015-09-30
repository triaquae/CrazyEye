
// Layouts.js
// ====================================================================
// Set the color themes to this page.
// This file is only used for demonstration purposes.
// ====================================================================
// - ThemeOn.net -



$(document).ready(function() {


	// Applying a theme
	// ================================
	changeTheme = function(themeName, type){
		var themeCSS = $('#theme'),
			filename = 'css/themes/type-'+type+'/'+themeName+'.min.css';

		if (themeCSS.length) {
			themeCSS.prop('href', filename);
		}else{
			themeCSS = '<link id="theme" href="'+filename+'" rel="stylesheet">';
			$('head').append(themeCSS);
		}
	};



	if($.cookie('settings-theme-name') && $.cookie('settings-theme-type')){
		changeTheme($.cookie('settings-theme-name'), $.cookie('settings-theme-type'));
	}

});
window.demoLayout = true;
