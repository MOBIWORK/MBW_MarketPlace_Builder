# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

MAX_BODY_LENGTH = 5000
SUCCEEDED = "succeeded"


class BuilderAIIngestLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		callback_payload: DF.Code | None
		callback_received: DF.Datetime | None
		error: DF.SmallText | None
		request_payload: DF.Code | None
		response_body: DF.Code | None
		response_status: DF.Int
		run_id: DF.Data | None
		status: DF.Literal["Pending", "Success", "Failed"]
		trace_id: DF.Data | None
		triggered_by: DF.Link | None
		website: DF.Data | None
	# end: auto-generated types

	def record(self, response=None, error=None):
		"""Ghi lại một lần gọi tạo run.

		2xx chỉ là dịch vụ AI nhận việc, chưa phải đã ingest xong, nên để Pending
		tới khi callback báo kết quả.
		"""
		self.triggered_by = frappe.session.user
		self.error = error

		if response is not None:
			self.response_status = response.status_code
			self.response_body = response.text[:MAX_BODY_LENGTH]
			self.status = "Pending" if response.ok else "Failed"
		else:
			self.status = "Failed"

		self.insert(ignore_permissions=True)
		return self

	def apply_callback(self, payload):
		"""Cập nhật log khi dịch vụ AI gọi callback báo kết quả của lô."""
		run = payload.get("run") or payload
		self.status = "Success" if run.get("status") == SUCCEEDED else "Failed"
		self.error = None if self.status == "Success" else run_error(run)
		self.callback_payload = frappe.as_json(payload)[:MAX_BODY_LENGTH]
		self.callback_received = frappe.utils.now_datetime()
		self.save(ignore_permissions=True)
		return self


def run_error(run):
	"""Thông điệp lỗi của run; `error` có thể là chuỗi hoặc dict tuỳ loại lỗi."""
	error = run.get("error")
	if isinstance(error, dict):
		return error.get("message") or frappe.as_json(error)
	return str(error) if error else f"Run {run.get('status') or 'failed'}"
