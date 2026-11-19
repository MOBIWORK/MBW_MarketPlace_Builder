"""Đồng bộ mẫu website sang dịch vụ AI qua Task API.

Người dùng chủ động bấm đồng bộ thay vì chạy tự động theo doc_events: dữ liệu
AI học là nội dung biên tập, thường được sửa qua nhiều lần lưu, nên để người
dùng chọn thời điểm "mẫu đã xong" là hợp lý hơn đẩy mọi bản nháp sang AI.

Chỉ gửi website_id; dịch vụ AI tự gọi ngược lại các endpoint trong
marketplace_api.py để lấy dữ liệu.

POST /v1/tasks/hr.website.template_ingest/runs chỉ nhận việc rồi trả run_id;
kết quả thật về sau qua callback_url nên log để Pending tới lúc đó.

File này nằm cạnh core, không sửa file core nào, nên merge upstream không xung đột.
"""

import uuid

import frappe
import requests

TASK_PATH = "/v1/tasks/hr.website.template_ingest/runs"
CALLBACK_METHOD = "builder.ai_ingest.ingest_callback"
CONCURRENCY = 1
REQUEST_TIMEOUT = 60
SUCCEEDED = "succeeded"


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
	"""Tạo 1 run cho cả lô rồi ghi vết cho từng mẫu.

	Lỗi kết nối được ném lên để người dùng thấy ngay tại chỗ — đây là hành
	động thủ công nên phản hồi tức thì quan trọng hơn việc nuốt lỗi.
	"""
	base_url, api_key = get_ai_config()
	trace_id = uuid.uuid4().hex
	payload = build_payload(website_ids, trace_id)

	try:
		response = requests.post(
			f"{base_url}{TASK_PATH}",
			headers=build_headers(api_key),
			json=payload,
			timeout=REQUEST_TIMEOUT,
		)
	except Exception as exc:
		log_batch(website_ids, payload, trace_id, error=frappe.get_traceback(with_context=False))
		frappe.throw(f"Không gọi được dịch vụ AI: {exc}")

	log_batch(website_ids, payload, trace_id, response=response)

	if not response.ok:
		frappe.throw(f"Dịch vụ AI trả về lỗi {response.status_code}: {response.text[:500]}")


def build_payload(website_ids, trace_id):
	return {
		"input": {
			"items": [{"website_id": name} for name in website_ids],
			"concurrency": CONCURRENCY,
		},
		"callback_url": build_callback_url(trace_id),
	}


def build_headers(api_key):
	"""Idempotency-Key sinh mới mỗi lần gọi: mỗi lô là một run riêng phía AI,
	dùng lại key sẽ bị coi là gửi trùng và trả về run cũ."""
	return {
		"X-API-Key": api_key,
		"Idempotency-Key": str(uuid.uuid4()),
		"Content-Type": "application/json",
	}


def build_callback_url(trace_id):
	"""trace_id nằm trên PATH chứ không ở query: callback gửi JSON nên form_dict bị
	thay bằng body, query string không vào tới handler. Chuỗi uuid này cũng là thứ
	duy nhất chặn request giả, vì endpoint callback không xác thực."""
	return f"{get_callback_base_url()}/api/method/{CALLBACK_METHOD}/{trace_id}"


def get_callback_base_url():
	"""Host để dịch vụ AI gọi ngược về. Sau tunnel/CDN thì khác URL site nên có
	ai_callback_host; không cấu hình thì lấy URL site và bỏ cổng dev của bench,
	vốn không gọi được từ ngoài."""
	host = frappe.conf.get("ai_callback_host")
	if host:
		return str(host).rstrip("/")
	return frappe.utils.get_url().replace(":8000", "").replace(":8080", "").rstrip("/")


def get_ai_config():
	base_url = frappe.conf.get("base_url_ai")
	api_key = frappe.conf.get("builder_ai_api_key")
	if not base_url or not api_key:
		frappe.throw("Chưa cấu hình base_url_ai và builder_ai_api_key trong site_config.json.")
	return base_url.rstrip("/"), api_key


def log_batch(website_ids, payload, trace_id, response=None, error=None):
	"""Ghi 1 dòng log cho mỗi mẫu để lọc được theo website."""
	run_id = extract_run_id(response)
	for name in website_ids:
		frappe.get_doc(
			{
				"doctype": "Builder AI Ingest Log",
				"website": name,
				"trace_id": trace_id,
				"run_id": run_id,
				"request_payload": frappe.as_json(payload),
			}
		).record(response=response, error=error)


def extract_run_id(response):
	if response is None or not response.ok:
		return None
	try:
		return (response.json() or {}).get("run_id")
	except ValueError:
		return None


@frappe.whitelist(methods=["POST"], allow_guest=True)
def ingest_callback(**kwargs):
	"""Dịch vụ AI gọi về khi chạy xong lô: cập nhật mọi log mang trace_id trên path.

	Endpoint không xác thực theo thiết kế của dịch vụ AI; trace_id trong URL là
	phần bí mật duy nhất nên không log nó ra ngoài.
	"""
	try:
		trace_id = trace_id_from_path()
		if not trace_id:
			return reply(400, "Thiếu trace_id")

		logs = frappe.get_all("Builder AI Ingest Log", filters={"trace_id": trace_id}, pluck="name")
		if not logs:
			return reply(404, "Không tìm thấy lô đồng bộ")

		payload = frappe.request.get_json(silent=True) or {}
		for name in logs:
			frappe.get_doc("Builder AI Ingest Log", name).apply_callback(payload)

		return reply(200, "OK")
	except Exception:
		frappe.log_error(title="Builder AI ingest callback error", message=frappe.get_traceback())
		return reply(500, "Lỗi xử lý callback")


def trace_id_from_path():
	path = (frappe.request.path if frappe.request else "") or ""
	marker = "ingest_callback/"
	if marker in path:
		return path.split(marker, 1)[1].strip("/").split("?")[0] or None
	return None


def reply(status_code, message):
	frappe.local.response["http_status_code"] = status_code
	return {"success": status_code < 400, "message": message}


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
