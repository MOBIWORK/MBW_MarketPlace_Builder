"""Đồng bộ mẫu website sang dịch vụ AI.

Người dùng chủ động bấm đồng bộ thay vì chạy tự động theo doc_events: dữ liệu
AI học là nội dung biên tập, thường được sửa qua nhiều lần lưu, nên để người
dùng chọn thời điểm "mẫu đã xong" là hợp lý hơn đẩy mọi bản nháp sang AI.

Chỉ gửi website_id; dịch vụ AI tự gọi ngược lại các endpoint trong
marketplace_api.py để lấy dữ liệu.

File này nằm cạnh core, không sửa file core nào, nên merge upstream không xung đột.
"""

import frappe
import requests

INGEST_PATH = "/builder_agent/api/v1/templates/ingest/batch"
REQUEST_TIMEOUT = 60


@frappe.whitelist()
def sync_websites(website_ids):
	"""Đẩy một hoặc nhiều mẫu website sang dịch vụ AI trong 1 request.

	Args:
		website_ids (str | list): tên Builder Website, hoặc chuỗi JSON của danh
			sách tên khi gọi từ giao diện.

	Returns:
		dict: {synced: [...], skipped: [...]} — skipped là các mẫu chưa published.
	"""
	frappe.only_for("System Manager")

	requested = parse_website_ids(website_ids)
	if not requested:
		frappe.throw("Chưa chọn mẫu website nào để đồng bộ.")

	published = filter_published(requested)
	skipped = [name for name in requested if name not in published]

	if published:
		send_batch(published)

	return {"synced": published, "skipped": skipped}


def parse_website_ids(website_ids):
	if isinstance(website_ids, str):
		website_ids = frappe.parse_json(website_ids)
	if isinstance(website_ids, str):
		website_ids = [website_ids]
	return list(dict.fromkeys(website_ids or []))


def filter_published(website_ids):
	"""Giữ nguyên thứ tự người dùng chọn, bỏ các mẫu chưa published."""
	published = set(
		frappe.get_all(
			"Builder Website",
			filters={"name": ["in", website_ids], "status": "published"},
			pluck="name",
		)
	)
	return [name for name in website_ids if name in published]


def send_batch(website_ids):
	"""Gửi 1 request cho cả lô rồi ghi vết cho từng mẫu.

	Lỗi kết nối được ném lên để người dùng thấy ngay tại chỗ — đây là hành
	động thủ công nên phản hồi tức thì quan trọng hơn việc nuốt lỗi.
	"""
	base_url, token = get_ai_config()
	payload = {"items": [{"website_id": name} for name in website_ids]}

	try:
		response = requests.post(
			f"{base_url}{INGEST_PATH}",
			headers={"Authorization": f"Bearer {token}"},
			json=payload,
			timeout=REQUEST_TIMEOUT,
		)
	except Exception as exc:
		log_batch(website_ids, payload, error=frappe.get_traceback(with_context=False))
		frappe.throw(f"Không gọi được dịch vụ AI: {exc}")

	log_batch(website_ids, payload, response=response)

	if not response.ok:
		frappe.throw(f"Dịch vụ AI trả về lỗi {response.status_code}: {response.text[:500]}")


def log_batch(website_ids, payload, response=None, error=None):
	"""Ghi 1 dòng log cho mỗi mẫu để lọc được theo website."""
	for name in website_ids:
		frappe.get_doc(
			{
				"doctype": "Builder AI Ingest Log",
				"website": name,
				"request_payload": frappe.as_json(payload),
			}
		).record(response=response, error=error)


def get_ai_config():
	base_url = frappe.conf.get("base_url_ai")
	token = frappe.conf.get("bear_auth_ai")
	if not base_url or not token:
		frappe.throw("Chưa cấu hình base_url_ai và bear_auth_ai trong site_config.json.")
	return base_url.rstrip("/"), token


@frappe.whitelist()
def get_last_sync(website_id):
	"""Lần đồng bộ gần nhất của một mẫu, để hiển thị trên form."""
	logs = frappe.get_all(
		"Builder AI Ingest Log",
		filters={"website": website_id},
		fields=["status", "creation", "triggered_by"],
		order_by="creation desc",
		limit=1,
	)
	return logs[0] if logs else None


def cleanup_old_logs():
	"""Xóa log của các tháng trước, chạy theo lịch đầu mỗi tháng."""
	first_day_of_month = frappe.utils.get_first_day(frappe.utils.nowdate())
	frappe.db.delete("Builder AI Ingest Log", {"creation": ["<", first_day_of_month]})
