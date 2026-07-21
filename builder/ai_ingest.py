"""Đồng bộ mẫu website sang dịch vụ AI.

Khi mẫu website thay đổi, đẩy website_id sang dịch vụ AI để nó tự gọi ngược
lại các endpoint trong marketplace_api.py mà lấy dữ liệu mới.

Chống gọi trùng theo 3 lớp:
1. Builder Website Page Item là child table nên Frappe không chạy doc_events
   riêng cho nó — sửa danh sách trang chỉ sinh 1 lần on_update ở website cha.
2. Builder Page chỉ kích hoạt khi các field trong PAGE_WATCHED_FIELDS đổi;
   draft_blocks cố tình nằm ngoài vì trình editor autosave liên tục.
3. Trong cùng request dùng frappe.flags, giữa các request dùng job_id +
   deduplicate của hàng đợi.

File này nằm cạnh core, không sửa file core nào, nên merge upstream không xung đột.
"""

import frappe

INGEST_PATH = "/builder_agent/api/v1/templates/ingest/batch"
REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 3

# Field của Builder Page ảnh hưởng tới dữ liệu AI học. draft_blocks bị loại
# vì editor autosave liên tục, đưa vào sẽ spam dịch vụ AI.
PAGE_WATCHED_FIELDS = ("route", "blocks", "page_title", "published")


def on_website_update(doc, method=None):
	if skip_ingest():
		return
	mark_for_ingest(doc.name, doc.doctype, doc.name)


def on_page_update(doc, method=None):
	if skip_ingest():
		return
	if not any(doc.has_value_changed(field) for field in PAGE_WATCHED_FIELDS):
		return
	mark_page_website_for_ingest(doc)


def on_page_trash(doc, method=None):
	if skip_ingest():
		return
	mark_page_website_for_ingest(doc)


def mark_page_website_for_ingest(page):
	website_id = find_website_of_page(page.name)
	if website_id:
		mark_for_ingest(website_id, page.doctype, page.name)


def find_website_of_page(page_name):
	"""Tra ngược Builder Page về Builder Website qua child table.

	Trả None khi trang không thuộc website nào — trang lẻ thì không đồng bộ.
	"""
	return frappe.db.get_value(
		"Builder Website Page Item",
		{"builder_page": page_name, "parenttype": "Builder Website"},
		"parent",
	)


def skip_ingest():
	"""Bỏ qua trong các tiến trình hệ thống.

	Thiếu guard này thì một lần bench migrate sẽ bắn hàng loạt request.
	"""
	flags = frappe.flags
	return bool(
		flags.in_migrate or flags.in_install or flags.in_patch or flags.in_test or flags.in_import
	)


def mark_for_ingest(website_id, trigger_doctype, trigger_docname):
	if not is_published(website_id):
		return
	if not get_ai_config():
		return
	if queued_in_this_request(website_id):
		return

	frappe.enqueue(
		"builder.ai_ingest.push_website",
		queue="short",
		job_id=f"ai-ingest::{website_id}",
		deduplicate=True,
		enqueue_after_commit=True,
		website_id=website_id,
		trigger_doctype=trigger_doctype,
		trigger_docname=trigger_docname,
	)


def is_published(website_id):
	return frappe.db.get_value("Builder Website", website_id, "status") == "published"


def queued_in_this_request(website_id):
	queued = frappe.flags.setdefault("ai_ingest_queued", set())
	if website_id in queued:
		return True
	queued.add(website_id)
	return False


def push_website(website_id, trigger_doctype=None, trigger_docname=None):
	log = frappe.new_doc("Builder AI Ingest Log")
	log.website = website_id
	log.trigger_doctype = trigger_doctype
	log.trigger_docname = trigger_docname
	log.insert(ignore_permissions=True)
	log.send_to_ai()


def get_ai_config():
	"""Đọc cấu hình dịch vụ AI từ site_config.json.

	Trả None khi chưa cấu hình để việc lưu website vẫn chạy bình thường trên
	máy dev — không được để thiếu config làm vỡ thao tác save.
	"""
	base_url = frappe.conf.get("base_url_ai")
	token = frappe.conf.get("bear_auth_ai")
	if not base_url or not token:
		return None
	return base_url.rstrip("/"), token


@frappe.whitelist()
def resync_website(website_id):
	"""Ép đồng bộ lại một website, bỏ qua mọi lớp chống trùng."""
	frappe.only_for("System Manager")
	if not get_ai_config():
		frappe.throw("Chưa cấu hình base_url_ai và bear_auth_ai trong site_config.json.")

	frappe.enqueue(
		"builder.ai_ingest.push_website",
		queue="short",
		website_id=website_id,
		trigger_doctype="Manual",
		trigger_docname=frappe.session.user,
	)
	return "queued"


def retry_failed_ingests():
	"""Thử lại các lần đồng bộ hỏng, chạy theo lịch mỗi giờ."""
	if not get_ai_config():
		return

	names = frappe.get_all(
		"Builder AI Ingest Log",
		filters={"status": "Failed", "attempts": ["<", MAX_ATTEMPTS]},
		pluck="name",
		order_by="creation asc",
		limit=50,
	)
	for name in names:
		frappe.get_doc("Builder AI Ingest Log", name).send_to_ai()


def cleanup_old_logs():
	"""Xóa log của các tháng trước, chạy theo lịch đầu mỗi tháng.

	Giữ lại bản ghi Failed còn hạn thử lại để không mất các lần đồng bộ hỏng.
	"""
	first_day_of_month = frappe.utils.get_first_day(frappe.utils.nowdate())
	logs = frappe.get_all(
		"Builder AI Ingest Log",
		filters={"creation": ["<", first_day_of_month]},
		or_filters=[
			["status", "=", "Success"],
			["attempts", ">=", MAX_ATTEMPTS],
		],
		pluck="name",
	)
	for name in logs:
		frappe.delete_doc("Builder AI Ingest Log", name, force=True, ignore_permissions=True)
