# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Template(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		builder_page: DF.Link | None
		description: DF.SmallText | None
		industry: DF.Link | None
		is_blog_detail: DF.Check
		is_blog_list: DF.Check
		is_featured: DF.Check
		is_homepage: DF.Check
		is_job_detail: DF.Check
		is_job_list: DF.Check
		purpose: DF.Literal["Recruitment", "Marketing", "Website"]
		sort_order: DF.Int
		status: DF.Literal["Draft", "Published", "Archived"]
		thumbnail: DF.AttachImage | None
		title: DF.Data
	# end: auto-generated types
	pass
