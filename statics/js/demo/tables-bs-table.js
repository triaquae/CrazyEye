
// Tables-BS-Table.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(document).ready(function() {


	// EDITABLE - COMBINATION WITH X-EDITABLE
	// =================================================================
	// Require X-editable
	// http://vitalets.github.io/x-editable/
	//
	// Require Bootstrap Table
	// http://bootstrap-table.wenzhixin.net.cn/
	//
	// Require X-editable Extension of Bootstrap Table
	// http://bootstrap-table.wenzhixin.net.cn/
	// =================================================================
	$('#demo-editable').bootstrapTable({
		idField: 'id',
		url: 'data/bs-table.json',
		columns: [{
			field: 'id',
			formatter:'invoiceFormatter',
			title: 'Invoice'
		}, {
			field: 'name',
			title: 'Name',
			editable: {
				type: 'text'
			}
		}, {
			field: 'date',
			title: 'Order date'
		}, {
			field: 'amount',
			title: 'Amount',
			editable: {
				type: 'text'
			}
		}, {
			field: 'status',
			align: 'center',
			title: 'Status',
			formatter:'statusFormatter'
		}, {
			field: 'track',
			title: 'Tracking Number',
			editable: {
				type: 'text'
			}
		}]
	});



	// X-EDITABLE USING FONT AWESOME ICONS
	// =================================================================
	// Require X-editable
	// http://vitalets.github.io/x-editable/
	//
	// Require Font Awesome
	// http://fortawesome.github.io/Font-Awesome/icons/
	// =================================================================
	$.fn.editableform.buttons =
		'<button type="submit" class="btn btn-primary editable-submit">'+
			'<i class="fa fa-fw fa-check"></i>'+
		'</button>'+
		'<button type="button" class="btn btn-default editable-cancel">'+
			'<i class="fa fa-fw fa-times"></i>'+
		'</button>';





	// BOOTSTRAP TABLE - USE NIFTYCHECK TO STYLE THE CHECKBOXES
	// =================================================================
	// Require nifty.js
	// =================================================================
	$(".demo-add-niftycheck").on('post-body.bs.table', function () {
		$(this).find('input:checkbox').not('.form-checkbox input:checkbox').wrap('<label class="form-checkbox form-icon"></label>');
		$(this).find('.form-checkbox').niftyCheck();
	});




	// BOOTSTRAP TABLE - USE NIFTYCHECK TO STYLE THE RADIOS
	// =================================================================
	// Require nifty.js
	// =================================================================
	$(".demo-add-niftyradio").on('post-body.bs.table', function () {
		$(this).find('input:radio').wrap('<label class="form-radio form-icon"></label>');
		$(this).find('.form-radio').niftyCheck();
	});





	// BOOTSTRAP TABLE - CUSTOM TOOLBAR
	// =================================================================
	// Require Bootstrap Table
	// http://bootstrap-table.wenzhixin.net.cn/
	// =================================================================
	var $table = $('#demo-custom-toolbar'),	$remove = $('#demo-delete-row');

	$table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function () {
		$remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
	});

	$remove.click(function () {
		var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
			return row.id
		});
		$table.bootstrapTable('remove', {
			field: 'id',
			values: ids
		});
		$remove.prop('disabled', true);
	});


});




// FORMAT COLUMN
// Use "data-formatter" on HTML to format the display of bootstrap table column.
// =================================================================


// Sample format for Invoice Column.
// =================================================================
function invoiceFormatter(value, row) {
	return '<a href="#" class="btn-link" > Order #' + value + '</a>';
}




// Sample Format for User Name Column.
// =================================================================
function nameFormatter(value, row) {
	return '<a href="#" class="btn-link" > ' + value + '</a>';
}




// Sample Format for Order Date Column.
// =================================================================
function dateFormatter(value, row) {
	var icon = row.id % 2 === 0 ? 'fa-star' : 'fa-user';
	return '<span class="text-muted"><i class="fa fa-clock-o"></i> ' + value + '</span>';
}



// Sample Format for Order Status Column.
// =================================================================
function statusFormatter(value, row) {
	var labelColor;
	if (value == "Paid") {
		labelColor = "success";
	}else if(value == "Unpaid"){
		labelColor = "warning";
	}else if(value == "Shipped"){
		labelColor = "info";
	}else if(value == "Refunded"){
		labelColor = "danger";
	}
	var icon = row.id % 2 === 0 ? 'fa-star' : 'fa-user';
	return '<div class="label label-table label-'+ labelColor+'"> ' + value + '</div>';
}



// Sample Format for Tracking Number Column.
// =================================================================
function trackFormatter(value, row) {
	if (value) return '<i class="fa fa-plane"></i> ' + value;
}



// Sort Price Column
// =================================================================
function priceSorter(a, b) {
	a = +a.substring(1); // remove $
	b = +b.substring(1);
	if (a > b) return 1;
	if (a < b) return -1;
	return 0;
}

