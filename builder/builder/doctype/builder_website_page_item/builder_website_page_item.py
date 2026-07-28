# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BuilderWebsitePageItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		builder_page: DF.Link | None
		is_blog_detail: DF.Check
		is_blog_list: DF.Check
		is_homepage: DF.Check
		is_job_detail: DF.Check
		is_job_list: DF.Check
		is_not_found: DF.Check
		is_privacy_policy: DF.Check
		is_terms_of_service: DF.Check
		is_thank_you: DF.Check
		order: DF.Int
		page_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		purpose: DF.SmallText | None
		sections_page: DF.JSON | None
		status: DF.Literal["draft", "published"]
	# end: auto-generated types
	pass
