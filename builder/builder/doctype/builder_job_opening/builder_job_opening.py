# Copyright (c) 2026, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BuilderJobOpening(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		deadline: DF.Data | None
		location: DF.Data | None
		remote: DF.Data | None
		salary: DF.Data | None
		title: DF.Data | None
	# end: auto-generated types
	pass
