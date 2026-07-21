# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

MAX_BODY_LENGTH = 5000


class BuilderAIIngestLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attempts: DF.Int
		error: DF.SmallText | None
		request_payload: DF.Code | None
		response_body: DF.Code | None
		response_status: DF.Int
		status: DF.Literal["Pending", "Success", "Failed"]
		trigger_docname: DF.Data | None
		trigger_doctype: DF.Data | None
		website: DF.Data | None
	# end: auto-generated types

	def send_to_ai(self):
		from builder.ai_ingest import INGEST_PATH, REQUEST_TIMEOUT, get_ai_config

		config = get_ai_config()
		if not config:
			return

		base_url, token = config
		payload = {"items": [{"website_id": self.website}]}

		self.request_payload = frappe.as_json(payload)
		self.attempts += 1
		self.error = None

		try:
			response = requests.post(
				f"{base_url}{INGEST_PATH}",
				headers={"Authorization": f"Bearer {token}"},
				json=payload,
				timeout=REQUEST_TIMEOUT,
			)
			self.record_response(response)
		except Exception:
			self.record_failure()

		self.save(ignore_permissions=True)

	def record_response(self, response):
		self.response_status = response.status_code
		self.response_body = response.text[:MAX_BODY_LENGTH]
		self.status = "Success" if response.ok else "Failed"

	def record_failure(self):
		self.status = "Failed"
		self.error = frappe.get_traceback(with_context=False)
		frappe.log_error(title=f"AI ingest failed: {self.website}")
