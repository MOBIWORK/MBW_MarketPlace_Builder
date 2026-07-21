// Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Builder Website", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status !== "published") return;

		frm.add_custom_button(__("Đồng bộ lại AI"), () => {
			frappe.call({
				method: "builder.ai_ingest.resync_website",
				args: { website_id: frm.doc.name },
				freeze: true,
				freeze_message: __("Đang gửi sang dịch vụ AI..."),
				callback: () => {
					frappe.show_alert({
						message: __("Đã gửi yêu cầu đồng bộ"),
						indicator: "green",
					});
				},
			});
		});
	},
});
