# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

MAX_BODY_LENGTH = 5000


class BuilderAIIngestLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		error: DF.SmallText | None
		request_payload: DF.Code | None
		response_body: DF.Code | None
		response_status: DF.Int
		status: DF.Literal["Success", "Failed"]
		triggered_by: DF.Link | None
		website: DF.Data | None
	# end: auto-generated types

	def record(self, response=None, error=None):
		"""Ghi lại kết quả một lần gọi dịch vụ AI."""
		self.triggered_by = frappe.session.user
		self.error = error

		if response is not None:
			self.response_status = response.status_code
			self.response_body = response.text[:MAX_BODY_LENGTH]
			self.status = "Success" if response.ok else "Failed"
		else:
			self.status = "Failed"

		self.insert(ignore_permissions=True)
		return self
