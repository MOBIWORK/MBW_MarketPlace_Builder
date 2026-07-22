// Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Builder Website", {
	refresh(frm) {
		if (frm.is_new()) return;

		frm.add_custom_button(__("Đồng bộ sang AI"), () => sync_to_ai(frm));
		show_last_sync(frm);
	},
});

function sync_to_ai(frm) {
	if (frm.doc.status !== "published") {
		frappe.msgprint({
			title: __("Chưa thể đồng bộ"),
			message: __("Chỉ mẫu ở trạng thái published mới được đẩy sang dịch vụ AI."),
			indicator: "orange",
		});
		return;
	}

	frappe.call({
		method: "builder.ai_ingest.sync_websites",
		args: { website_ids: [frm.doc.name] },
		freeze: true,
		freeze_message: __("Đang gửi sang dịch vụ AI..."),
		callback: () => {
			frappe.show_alert({ message: __("Đã đồng bộ sang AI"), indicator: "green" });
			show_last_sync(frm);
		},
	});
}

function show_last_sync(frm) {
	frappe.call({
		method: "builder.ai_ingest.get_last_sync",
		args: { website_id: frm.doc.name },
		callback: ({ message }) => {
			if (!message) {
				frm.dashboard.set_headline(__("Chưa đồng bộ sang AI lần nào."));
				return;
			}

			const when = frappe.datetime.prettyDate(message.creation);
			const label =
				message.status === "Success"
					? __("Đồng bộ AI thành công {0}", [when])
					: __("Lần đồng bộ AI gần nhất thất bại ({0})", [when]);

			frm.dashboard.set_headline(label);
		},
	});
}
