
// Form-Validation.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).ready(function() {


	// FORM VALIDATION
	// =================================================================
	// Require Bootstrap Validator
	// http://bootstrapvalidator.com/
	// =================================================================


	// FORM VALIDATION FEEDBACK ICONS
	// =================================================================
	var faIcon = {
		valid: 'fa fa-check-circle fa-lg text-success',
		invalid: 'fa fa-times-circle fa-lg',
		validating: 'fa fa-refresh'
	}



	// FORM VALIDATION ON TABS
	// =================================================================
	$('#demo-bv-bsc-tabs').bootstrapValidator({
		excluded: [':disabled'],
		feedbackIcons: faIcon,
		fields: {
		fullName: {
			validators: {
				notEmpty: {
					message: 'The full name is required'
				}
			}
		},
		company: {
			validators: {
				notEmpty: {
					message: 'The company name is required'
				}
			}
		},
		memberType: {
			validators: {
				notEmpty: {
					message: 'Please choose the membership type that best meets your needs'
				}
			}
		},
		address: {
			validators: {
				notEmpty: {
					message: 'The address is required'
				}
			}
		},
		city: {
			validators: {
				notEmpty: {
					message: 'The city is required'
				}
			}
		},
		country: {
			validators: {
				notEmpty: {
					message: 'The city is required'
				}
			}
		}
		}
	}).on('status.field.bv', function(e, data) {
		var $form     = $(e.target),
		validator = data.bv,
		$tabPane  = data.element.parents('.tab-pane'),
		tabId     = $tabPane.attr('id');

		if (tabId) {
		var $icon = $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i');

		// Add custom class to tab containing the field
		if (data.status == validator.STATUS_INVALID) {
			$icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
		} else if (data.status == validator.STATUS_VALID) {
			var isValidTab = validator.isValidContainer($tabPane);
			$icon.removeClass(faIcon.valid).addClass(isValidTab ? faIcon.valid : faIcon.invalid);
		}
		}
	});


	// FORM VALIDATION ON ACCORDION
	// =================================================================
	$('#demo-bv-accordion').bootstrapValidator({
		message: 'This value is not valid',
		excluded: ':disabled',
		feedbackIcons: faIcon,
		fields: {
		firstName: {
			validators: {
				notEmpty: {
					message: 'The first name is required and cannot be empty'
				},
				regexp: {
					regexp: /^[A-Z\s]+$/i,
					message: 'The first name can only consist of alphabetical characters and spaces'
				}
			}
		},
		lastName: {
			validators: {
				notEmpty: {
					message: 'The last name is required and cannot be empty'
				},
				regexp: {
					regexp: /^[A-Z\s]+$/i,
					message: 'The last name can only consist of alphabetical characters and spaces'
				}
			}
		},
		username: {
			message: 'The username is not valid',
			validators: {
				notEmpty: {
					message: 'The username is required and cannot be empty'
				},
				stringLength: {
					min: 4,
					max: 30,
					message: 'The username must be more than 4 and less than 30 characters long'
				},
				regexp: {
					regexp: /^[a-zA-Z0-9_\.]+$/,
					message: 'The username can only consist of alphabetical, number, dot and underscore'
				},
				different: {
					field: 'password',
					message: 'The username and password cannot be the same as each other'
				}
			}
		},
		email: {
			validators: {
				notEmpty: {
					message: 'The email address is required and cannot be empty'
				},
				emailAddress: {
					message: 'The input is not a valid email address'
				}
			}
		},
		password: {
			validators: {
				notEmpty: {
					message: 'The password is required and cannot be empty'
				},
				different: {
					field: 'username',
					message: 'The password cannot be the same as username'
				}
			}
		},
		memberType: {
			validators: {
				notEmpty: {
					message: 'The gender is required'
				}
			}
		},
		bio:{
			validators: {
				notEmpty: {
					message: 'The bio is required and cannot be empty'
				},
			}
		},
		phoneNumber: {
			validators: {
				notEmpty: {
					message: 'The phone number is required and cannot be empty'
				},
				digits: {
					message: 'The value can contain only digits'
				}
			}
		},
		city:{
			validators: {
				notEmpty: {
					message: 'The city is required and cannot be empty'
				},
			}
		}
		}
	}).on('status.field.bv', function(e, data) {
		var $form = $(e.target),
		validator = data.bv,
		$collapsePane = data.element.parents('.collapse'),
		colId = $collapsePane.attr('id');

		if (colId) {
		var $anchor = $('a[href="#' + colId + '"][data-toggle="collapse"]');
		var $icon = $anchor.find('i');

		// Add custom class to panel containing the field
		if (data.status == validator.STATUS_INVALID) {
			$anchor.addClass('bv-col-error');
			$icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
		} else if (data.status == validator.STATUS_VALID) {
			var isValidCol = validator.isValidContainer($collapsePane);
			if (isValidCol) {
				$anchor.removeClass('bv-col-error');
			}else{
				$anchor.addClass('bv-col-error');
			}
			$icon.removeClass(faIcon.valid + " " + faIcon.invalid).addClass(isValidCol ? faIcon.valid : faIcon.invalid);
		}
		}
	});


	// FORM VALIDATION CUSTOM ERROR CONTAINER
	// =================================================================
	// Indicate where the error messages are shown.
	// Tooltip, Popover, Custom Container.
	// =================================================================
	$('#demo-bv-errorcnt').bootstrapValidator({
		message: 'This value is not valid',
		excluded: [':disabled'],
		feedbackIcons: faIcon,
		fields: {
		name: {
			container: 'tooltip',
			validators: {
				notEmpty: {
					message: 'The first name is required and cannot be empty'
				},
				regexp: {
					regexp: /^[A-Z\s]+$/i,
					message: 'The first name can only consist of alphabetical characters and spaces'
				}
			}
		},
		lastName: {
			validators: {
				notEmpty: {
					message: 'The last name is required and cannot be empty'
				},
				regexp: {
					regexp: /^[A-Z\s]+$/i,
					message: 'The last name can only consist of alphabetical characters and spaces'
				}
			}
		},
		email: {
			container: 'tooltip',
			validators: {
				notEmpty: {
					message: 'The email address is required and can\'t be empty'
				},
				emailAddress: {
					message: 'The input is not a valid email address'
				}
			}
		},
		username: {
			container: 'popover',
			message: 'The username is not valid',
			validators: {
				notEmpty: {
					message: 'The username is required and cannot be empty'
				},
				stringLength: {
					min: 6,
					max: 30,
					message: 'The username must be more than 6 and less than 30 characters long'
				},
				regexp: {
					regexp: /^[a-zA-Z0-9_\.]+$/,
					message: 'The username can only consist of alphabetical, number, dot and underscore'
				},
				different: {
					field: 'password',
					message: 'The username and password cannot be the same as each other'
				}
			}
			},
		password: {
			container: 'popover',
				validators: {
					notEmpty: {
					message: 'The password is required and cannot be empty'
					},
					different: {
						field: 'username',
						message: 'The password cannot be the same as username'
					}
				}
		},
		phoneNumber: {
			container: '#demo-error-container',
			validators: {
				notEmpty: {
					message: 'The phone number is required and cannot be empty'
				},
				digits: {
					message: 'The value can contain only digits'
				}
				}
		},
		city:{
			container: '#demo-error-container',
			validators: {
				notEmpty: {
					message: 'The city is required and cannot be empty'
				},
			}
		}
		}
	}).on('status.field.bv', function(e, data) {
		var $form     = $(e.target),
		validator = data.bv,
		$tabPane  = data.element.parents('.tab-pane'),
		tabId     = $tabPane.attr('id');

		if (tabId) {
		var $icon = $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i');
		// Add custom class to tab containing the field
		if (data.status == validator.STATUS_INVALID) {
			$icon.removeClass(faIcon.valid).addClass(faIcon.invalid);
		} else if (data.status == validator.STATUS_VALID) {
			var isValidTab = validator.isValidContainer($tabPane);
			$icon.removeClass(faIcon.valid).addClass(isValidTab ? faIcon.valid : faIcon.invalid);
		}
		}
	});


	// FORM VARIOUS VALIDATION
	// =================================================================
	$('#demo-bvd-notempty').bootstrapValidator({
		message: 'This value is not valid',
		feedbackIcons: faIcon,
		fields: {
		username: {
			message: 'The username is not valid',
			validators: {
				notEmpty: {
					message: 'The username is required.'
				}
			}
		},
		acceptTerms: {
			validators: {
				notEmpty: {
					message: 'You have to accept the terms and policies'
				}
			}
		},
		password: {
			validators: {
				notEmpty: {
					message: 'The password is required and can\'t be empty'
				},
				identical: {
					field: 'confirmPassword',
					message: 'The password and its confirm are not the same'
				}
			}
		},
		confirmPassword: {
			validators: {
				notEmpty: {
					message: 'The confirm password is required and can\'t be empty'
				},
				identical: {
					field: 'password',
					message: 'The password and its confirm are not the same'
				}
			}
		},
		member: {
			validators: {
				notEmpty: {
					message: 'The gender is required'
				}
			}
		},
		'programs[]': {
			validators: {
				choice: {
					min: 2,
					max: 4,
					message: 'Please choose 2 - 4 programming languages you are good at'
				}
			}
		},
		integer: {
			validators: {
				notEmpty: {
					message: 'The number is required and can\'t be empty'
				},
				integer: {
					message: 'The value is not a number'
				}
			}
		},
		numeric: {
			validators: {
				notEmpty: {
					message: 'The number is required and can\'t be empty'
				},
				numeric: {
					message: 'The value is not a number'
				}
			}
		},
		greaterthan: {
			validators: {
				notEmpty: {
					message: 'The number is required and can\'t be empty'
				},
				greaterThan: {
					inclusive:false,
					//If true, the input value must be greater than or equal to the comparison one.
					//If false, the input value must be greater than the comparison one
					value: 50,
					message: 'Please enter a value greater than 50'
				}
			}
		},
		lessthan: {
			validators: {
				notEmpty: {
					message: 'The number is required and can\'t be empty'
				},
				lessThan: {
					inclusive:false,
					//If true, the input value must be less than or equal to the comparison one.
					//If false, the input value must be less than the comparison one
					value: 25,
					message: 'Please enter a value less than 25'
				}
			}
		},
		range: {
			validators: {
				inclusive:true,
				notEmpty: {
					message: 'The number is required and can\'t be empty'
				},
				between: {
					min:1,
					max:100,
					message: 'Please enter a number between 1 and 100'
				}
			}
		},
		uppercase:{
			validators: {
				notEmpty: {
					message: 'The card holder is required and can\'t be empty'
				},
				// Since case is a Javascript keyword,
				// you should place it between quotes (like 'case' or "case")
				// to make it work in all browsers
				stringCase: {
					message: 'The card holder must be in uppercase',
					'case': 'upper'
				}
			}
		},
		email: {
			validators: {
				notEmpty: {
					message: 'The email address is required and can\'t be empty'
				},
				emailAddress: {
					message: 'The input is not a valid email address'
				}
			}
		},
		website: {
			validators: {
				notEmpty: {
					message: 'The website address is required and can\'t be empty'
				},
				uri: {
					allowLocal: false,
					message: 'The input is not a valid URL'
				}
			}
		},
		color: {
			validators: {
				notEmpty: {
					message: 'The hex color is required and can\'t be empty'
				},
				hexColor: {
					message: 'The input is not a valid hex color'
				}
			}
		}
		}
	}).on('success.field.bv', function(e, data) {
		// $(e.target)  --> The field element
		// data.bv      --> The BootstrapValidator instance
		// data.field   --> The field name
		// data.element --> The field element

		var $parent = data.element.parents('.form-group');

		// Remove the has-success class
		$parent.removeClass('has-success');
	});




	// MASKED INPUT
	// =================================================================
	// Require Masked Input
	// http://digitalbush.com/projects/masked-input-plugin/
	// =================================================================


	// Initialize Masked Inputs
	// a - Represents an alpha character (A-Z,a-z)
	// 9 - Represents a numeric character (0-9)
	// * - Represents an alphanumeric character (A-Z,a-z,0-9)
	$('#demo-msk-date').mask('99/99/9999');
	$('#demo-msk-date2').mask('99-99-9999');
	$('#demo-msk-phone').mask('(999) 999-9999');
	$('#demo-msk-phone-ext').mask('(999) 999-9999? x99999');
	$('#demo-msk-taxid').mask('99-9999999');
	$('#demo-msk-ssn').mask('999-99-9999');
	$('#demo-msk-pkey').mask('a*-999-a999');



});
