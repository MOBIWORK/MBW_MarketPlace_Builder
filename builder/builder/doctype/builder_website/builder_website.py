# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BuilderWebsite(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from builder.builder.doctype.builder_website_page_item.builder_website_page_item import BuilderWebsitePageItem
		from frappe.types import DF

		category: DF.Link | None
		description: DF.SmallText | None
		domain: DF.Data | None
		favicon: DF.Attach | None
		logo: DF.Attach | None
		pages: DF.Table[BuilderWebsitePageItem]
		preview_url: DF.Data | None
		status: DF.Literal["draft", "published"]
		thumbnail: DF.AttachImage | None
		title: DF.Data | None
	# end: auto-generated types
	pass
