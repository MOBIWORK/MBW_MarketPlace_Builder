frappe.pages['blog-listing'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Bog',
		single_column: true
	});
}