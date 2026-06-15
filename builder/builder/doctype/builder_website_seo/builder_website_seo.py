# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BuilderWebsiteSEO(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		keywords: DF.JSON | None
		meta_description: DF.SmallText | None
		meta_title: DF.Data | None
		og_description: DF.SmallText | None
		og_image: DF.AttachImage | None
		og_title: DF.Data | None
		robots: DF.Attach | None
		sitemap_enabled: DF.Check
		website: DF.Link | None
	# end: auto-generated types
	pass
