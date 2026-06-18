# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BuilderBlogPost(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		author: DF.Data | None
		category: DF.Data | None
		description: DF.SmallText | None
		publish_time: DF.Data | None
		sub_description: DF.Data | None
		thumbnail: DF.AttachImage | None
		title: DF.Data | None
	# end: auto-generated types
	pass
