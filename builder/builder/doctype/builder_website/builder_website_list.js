// Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.listview_settings["Builder Website"] = {
	onload(listview) {
		listview.page.add_actions_menu_item(__("Đồng bộ sang AI"), () => {
			const names = listview.get_checked_items(true);
			if (!names.length) return;

			frappe.call({
				method: "builder.ai_ingest.sync_websites",
				args: { website_ids: names },
				freeze: true,
				freeze_message: __("Đang gửi sang dịch vụ AI..."),
				callback: ({ message }) => {
					if (message.skipped.length) {
						frappe.msgprint({
							title: __("Đã đồng bộ {0} mẫu", [message.synced.length]),
							message: __("Bỏ qua {0} mẫu chưa published: {1}", [
								message.skipped.length,
								message.skipped.join(", "),
							]),
							indicator: "orange",
						});
					} else {
						frappe.show_alert({
							message: __("Đã đồng bộ {0} mẫu sang AI", [message.synced.length]),
							indicator: "green",
						});
					}
					listview.refresh();
				},
			});
		});
	},
};
