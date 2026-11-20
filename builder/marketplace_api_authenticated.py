"""Bản có xác thực của các endpoint dữ liệu mẫu website.

marketplace_api.py vẫn giữ allow_guest cho những consumer công khai đang dùng;
file này không sửa file đó mà bọc lại đúng logic cũ rồi thêm xác thực, dành cho
dịch vụ AI pull dữ liệu đầy đủ (block, SEO, design token).

Gọi bằng API key của một User trong Frappe:

	Authorization: token <api_key>:<api_secret>

Bỏ allow_guest chỉ chặn được khách. Site này còn Website User (ứng viên) nên
phải chặn tiếp theo quyền doctype, thay vì coi "đã đăng nhập" là đủ.
"""

import frappe

from builder import marketplace_api

BRIEF_DOCTYPES = ("Builder Website", "Builder Page")
DETAIL_DOCTYPES = (*BRIEF_DOCTYPES, "Builder Website SEO")
VARIABLE_DOCTYPES = ("Builder Variable",)


def check_read_access(doctypes):
	"""Ném PermissionError nếu user không đọc được doctype mà endpoint trả về.

	Dựa luôn vào quyền doctype sẵn có thay vì định nghĩa role mới: ai xem được
	mẫu website trong desk thì gọi được API này.
	"""
	for doctype in doctypes:
		frappe.has_permission(doctype, "read", throw=True)


@frappe.whitelist(methods=["GET"])
def get_website_detail(website_id):
	"""Như marketplace_api.get_website_detail nhưng yêu cầu xác thực."""
	check_read_access(DETAIL_DOCTYPES)
	return marketplace_api.get_website_detail(website_id)


@frappe.whitelist(methods=["GET"])
def get_website_content_brief(website_id):
	"""Như marketplace_api.get_website_content_brief nhưng yêu cầu xác thực."""
	check_read_access(BRIEF_DOCTYPES)
	return marketplace_api.get_website_content_brief(website_id)


@frappe.whitelist(methods=["GET"])
def get_builder_variables():
	"""Như marketplace_api.get_builder_variables nhưng yêu cầu xác thực."""
	check_read_access(VARIABLE_DOCTYPES)
	return marketplace_api.get_builder_variables()
