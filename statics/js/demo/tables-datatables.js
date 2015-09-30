
// Tables-DataTables.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(window).on('load', function() {


	// DATA TABLES
	// =================================================================
	// Require Data Tables
	// -----------------------------------------------------------------
	// http://www.datatables.net/
	// =================================================================

	$.fn.DataTable.ext.pager.numbers_length = 5;


	// Basic Data Tables with responsive plugin
	// -----------------------------------------------------------------
	$('#demo-dt-basic').dataTable( {
		"responsive": true,
		"language": {
			"paginate": {
			  "previous": '<i class="fa fa-angle-left"></i>',
			  "next": '<i class="fa fa-angle-right"></i>'
			}
		}
	} );





	// Row selection (single row)
	// -----------------------------------------------------------------
	var rowSelection = $('#demo-dt-selection').DataTable({
		"responsive": true,
		"language": {
			"paginate": {
			  "previous": '<i class="fa fa-angle-left"></i>',
			  "next": '<i class="fa fa-angle-right"></i>'
			}
		}
	});

	$('#demo-dt-selection').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			$(this).removeClass('selected');
		}
		else {
			rowSelection.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
		}
	} );






	// Row selection and deletion (multiple rows)
	// -----------------------------------------------------------------
	var rowDeletion = $('#demo-dt-delete').DataTable({
		"responsive": true,
		"language": {
			"paginate": {
			  "previous": '<i class="fa fa-angle-left"></i>',
			  "next": '<i class="fa fa-angle-right"></i>'
			}
		},
		"dom": '<"toolbar">frtip'
	});
	$('#demo-custom-toolbar').appendTo($("div.toolbar"));

	$('#demo-dt-delete tbody').on( 'click', 'tr', function () {
		$(this).toggleClass('selected');
	} );

	$('#demo-dt-delete-btn').click( function () {
		rowDeletion.row('.selected').remove().draw( false );
	} );






	// Add Row
	// -----------------------------------------------------------------
	var t = $('#demo-dt-addrow').DataTable({
		"responsive": true,
		"language": {
			"paginate": {
			  "previous": '<i class="fa fa-angle-left"></i>',
			  "next": '<i class="fa fa-angle-right"></i>'
			}
		},
		"dom": '<"newtoolbar">frtip'
	});
	$('#demo-custom-toolbar2').appendTo($("div.newtoolbar"));

	$('#demo-dt-addrow-btn').on( 'click', function () {
		t.row.add( [
			'Adam Doe',
			'New Row',
			'New Row',
			nifty.randomInt(1,100),
			'2015/10/15',
			'$' + nifty.randomInt(1,100) +',000'
		] ).draw();
	} );


});
