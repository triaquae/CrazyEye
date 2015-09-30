
// Tables-FooTable.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -



$(window).on('load', function() {


	// FOO TABLES
	// =================================================================
	// Require FooTable
	// -----------------------------------------------------------------
	// http://fooplugins.com/footable-demos/
	// =================================================================


	// Row Toggler
	// -----------------------------------------------------------------
	$('#demo-foo-row-toggler').footable();




	// Expand / Collapse All Rows
	// -----------------------------------------------------------------
	var fooColExp = $('#demo-foo-col-exp');
	fooColExp.footable().trigger('footable_expand_first_row');


	$('#demo-foo-collapse').on('click', function(){
		fooColExp.trigger('footable_collapse_all');
	});
	$('#demo-foo-expand').on('click', function(){
		fooColExp.trigger('footable_expand_all');
	})





	// Accordion
	// -----------------------------------------------------------------
	$('#demo-foo-accordion').footable().on('footable_row_expanded', function(e) {
		$('#demo-foo-accordion tbody tr.footable-detail-show').not(e.row).each(function() {
			$('#demo-foo-accordion').data('footable').toggleDetail(this);
		});
	});





	// Pagination
	// -----------------------------------------------------------------
	$('#demo-foo-pagination').footable();
	$('#demo-show-entries').change(function (e) {
		e.preventDefault();
		var pageSize = $(this).val();
		$('#demo-foo-pagination').data('page-size', pageSize);
		$('#demo-foo-pagination').trigger('footable_initialized');
	});







	// Filtering
	// -----------------------------------------------------------------
	var filtering = $('#demo-foo-filtering');
	filtering.footable().on('footable_filtering', function (e) {
		var selected = $('#demo-foo-filter-status').find(':selected').val();
		e.filter += (e.filter && e.filter.length > 0) ? ' ' + selected : selected;
		e.clear = !e.filter;
	});

	// Filter status
	$('#demo-foo-filter-status').change(function (e) {
		e.preventDefault();
		filtering.trigger('footable_filter', {filter: $(this).val()});
	});

	// Search input
	$('#demo-foo-search').on('input', function (e) {
		e.preventDefault();
		filtering.trigger('footable_filter', {filter: $(this).val()});
	});








	// Add & Remove Row
	// -----------------------------------------------------------------
	var addrow = $('#demo-foo-addrow');
	addrow.footable().on('click', '.demo-delete-row', function() {

		//get the footable object
		var footable = addrow.data('footable');

		//get the row we are wanting to delete
		var row = $(this).parents('tr:first');

		//delete the row
		footable.removeRow(row);
	});

	// Search input
	$('#demo-input-search2').on('input', function (e) {
		e.preventDefault();
		addrow.trigger('footable_filter', {filter: $(this).val()});
	});

	// Add Row Button
	$('#demo-btn-addrow').click(function() {

		//get the footable object
		var footable = addrow.data('footable');

		//build up the row we are wanting to add
		var newRow = '<tr><td><button class="demo-delete-row btn btn-danger btn-xs btn-icon fa fa-times"></button></td><td>Adam</td><td>Doe</td><td>Traffic Court Referee</td><td>22 Jun 1972</td><td><span class="label label-table label-success">Active</span></td></tr>';

		//add it
		footable.appendRow(newRow);
	});
});
