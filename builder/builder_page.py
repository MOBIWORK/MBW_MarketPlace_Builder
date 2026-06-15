import frappe
import uuid
import json

def _generate_block_id():
	"""Generate a short random block ID similar to the builder's format."""
	return uuid.uuid4().hex[:9]


def _build_job_block(job):
	"""
	Build a single job card block structure based on the provided job data.

	:param job: dict with keys job_title, job_typework, job_location,
	            job_deadline, job_salary, link_job
	"""
	job_title = job.get("job_title", "")
	job_typework = job.get("job_typework", "")
	job_location = job.get("job_location", "")
	job_deadline = job.get("job_deadline", "")
	job_salary = job.get("job_salary")
	link_job = job.get("link_job", "")

	# Resolve salary display
	if job_salary is None:
		salary_html = "\nLương thỏa thuận\n\n"
		salary_color = "#000000"
	else:
		salary_html = f"\n{job_salary}\n\n"
		salary_color = "#5d93de"

	block = {
		"blockId": _generate_block_id(),
		"children": [
			# --- job_title ---
			{
				"blockId": _generate_block_id(),
				"children": [],
				"baseStyles": {
					"fontSize": "19px",
					"width": "fit-content",
					"height": "fit-content",
					"lineHeight": "1.4",
					"minWidth": "10px",
					"position": "static",
					"color": "#05264e",
					"fontWeight": "400",
					"fontFamily": "200",
					"padding": "20px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"element": "p",
				"innerHTML": f"\n{job_title}\n\n",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {"id_element": "job_title"},
			},
			# --- job_work_from (job_typework label placeholder) ---
			{
				"blockId": _generate_block_id(),
				"children": [],
				"baseStyles": {
					"fontSize": "18px ",
					"width": "fit-content",
					"height": "fit-content",
					"lineHeight": "1.4",
					"minWidth": "10px",
					"position": "static",
					"textAlign": "left",
					"color": "#4f5e64",
					"paddingTop": "0px",
					"paddingRight": "0px",
					"paddingBottom": "0px",
					"paddingLeft": "15px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"element": "p",
				"innerHTML": "",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {"id_element": "job_work_from"},
			},
			# --- grid row: typework + location ---
			{
				"blockId": _generate_block_id(),
				"children": [
					{
						"blockId": _generate_block_id(),
						"children": [],
						"baseStyles": {
							"fontSize": "17px",
							"width": "fit-content",
							"height": "fit-content",
							"lineHeight": "1.4",
							"minWidth": "10px",
							"position": "static",
							"textAlign": "left",
							"color": "#4f5e64",
							"paddingTop": "0pc",
							"paddingRight": "0px",
							"paddingBottom": "0px",
							"paddingLeft": "20px",
						},
						"rawStyles": {},
						"mobileStyles": {},
						"tabletStyles": {},
						"attributes": {},
						"classes": [],
						"dataKey": None,
						"element": "p",
						"innerHTML": f"\n{job_typework}\n\n",
						"activeState": None,
						"dynamicValues": [],
						"customAttributes": {"id_element": "job_typework"},
					},
					{
						"blockId": _generate_block_id(),
						"children": [],
						"baseStyles": {
							"fontSize": "17px",
							"width": "fit-content",
							"height": "fit-content",
							"lineHeight": "1.4",
							"minWidth": "10px",
							"position": "static",
							"textAlign": "left",
							"color": "#4f5e64",
							"paddingTop": "0pc",
							"paddingRight": "0px",
							"paddingBottom": "0px",
							"paddingLeft": "20px",
						},
						"rawStyles": {},
						"mobileStyles": {},
						"tabletStyles": {},
						"attributes": {},
						"classes": [],
						"dataKey": None,
						"element": "p",
						"innerHTML": f"\n{job_location}\n\n",
						"activeState": None,
						"dynamicValues": [],
						"customAttributes": {"id_element": "job_location"},
					},
				],
				"baseStyles": {
					"display": "grid",
					"flexDirection": "column",
					"flexShrink": 0,
					"overflow": "hidden",
					"position": "static",
					"backgroundColor": "#ffffff",
					"width": "313px",
					"height": "39px",
					"gridTemplateColumns": "repeat(2, minmax(200px, 1fr))",
					"gap": "10px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"blockName": "container",
				"element": "div",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {},
			},
			# --- job_deadline ---
			{
				"blockId": _generate_block_id(),
				"children": [],
				"baseStyles": {
					"fontSize": "17px",
					"width": "fit-content",
					"height": "fit-content",
					"lineHeight": "1.4",
					"minWidth": "10px",
					"position": "static",
					"textAlign": "left",
					"color": "#4f5e64",
					"paddingTop": "0pc",
					"paddingRight": "0px",
					"paddingBottom": "0px",
					"paddingLeft": "20px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"element": "p",
				"innerHTML": f"\nThời hạn: {job_deadline}\n\n",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {"id_element": "job_deadline"},
			},
			# --- horizontal divider ---
			{
				"blockId": _generate_block_id(),
				"children": [],
				"baseStyles": {
					"display": "flex",
					"flexDirection": "column",
					"flexShrink": 0,
					"overflow": "hidden",
					"position": "static",
					"backgroundColor": "#c7c7c7",
					"height": "1px",
					"padding": "0px",
					"margin": "15px",
					"marginRight": "0px",
					"width": "299px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"blockName": "container",
				"element": "div",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {},
			},
			# --- footer row: salary + apply button ---
			{
				"blockId": _generate_block_id(),
				"children": [
					# salary
					{
						"blockId": _generate_block_id(),
						"children": [],
						"baseStyles": {
							"fontSize": "20px",
							"width": "fit-content",
							"height": "fit-content",
							"lineHeight": "1.4",
							"minWidth": "10px",
							"color": salary_color,
							"paddingTop": "0px",
							"paddingRight": "0px",
							"paddingBottom": "0px",
							"paddingLeft": "15px",
						},
						"rawStyles": {},
						"mobileStyles": {},
						"tabletStyles": {},
						"attributes": {},
						"classes": [],
						"dataKey": None,
						"element": "p",
						"innerHTML": salary_html,
						"activeState": None,
						"dynamicValues": [],
						"customAttributes": {"id_element": "job_salary"},
					},
					# apply button wrapper
					{
						"blockId": _generate_block_id(),
						"children": [
							{
								"blockId": _generate_block_id(),
								"children": [],
								"baseStyles": {
									"color": "var(--neutral-white, #FFF)",
									"fontSize": "14px",
									"fontWeight": "420",
									"height": "fit-content",
									"left": "auto",
									"letterSpacing": "0.28px",
									"lineHeight": "115%",
									"minWidth": "30px",
									"position": "static",
									"top": "auto",
									"width": "fit-content",
								},
								"rawStyles": {},
								"mobileStyles": {},
								"tabletStyles": {},
								"attributes": {},
								"classes": ["__text_block__"],
								"dataKey": None,
								"element": "p",
								"innerHTML": "\nỨng tuyển\n\n",
								"activeState": None,
								"dynamicValues": [],
								"customAttributes": {},
							}
						],
						"baseStyles": {
							"alignItems": "center",
							"borderRadius": "4px",
							"display": "flex",
							"flexDirection": "column",
							"height": "fit-content",
							"justifyContent": "center",
							"padding": "6px 8px",
							"width": "fit-content",
							"backgroundColor": "#171717",
						},
						"rawStyles": {
							"flex-shrink": "0",
							"hover:background": "#383838",
							"transition": "all 0.1s ease-out",
						},
						"mobileStyles": {},
						"tabletStyles": {},
						"attributes": {"href": link_job},
						"classes": ["__text_block__"],
						"dataKey": None,
						"blockName": "button-link",
						"element": "a",
						"activeState": None,
						"dynamicValues": [],
						"customAttributes": {"id_element": "job_apply"},
					},
				],
				"baseStyles": {
					"display": "grid",
					"flexDirection": "column",
					"flexShrink": 0,
					"overflow": "hidden",
					"position": "static",
					"backgroundColor": "#ffffff",
					"width": "317px",
					"gridTemplateColumns": "repeat(2, minmax(200px, 1fr))",
					"gap": "30px",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"attributes": {},
				"classes": [],
				"dataKey": None,
				"blockName": "container",
				"element": "div",
				"activeState": None,
				"dynamicValues": [],
				"customAttributes": {},
			},
		],
		"baseStyles": {
			"borderRadius": "30px",
			"display": "flex",
			"flexDirection": "column",
			"flexShrink": 0,
			"height": "100%",
			"overflow": "hidden",
			"position": "static",
			"width": "auto",
			"overflowX": "hidden",
			"overflowY": "hidden",
			"backgroundColor": "#ffffff",
		},
		"rawStyles": {},
		"mobileStyles": {},
		"tabletStyles": {},
		"attributes": {"href": link_job},
		"classes": [],
		"dataKey": None,
		"blockName": "cell-1",
		"element": "a",
		"elementBeforeConversion": "div",
		"activeState": None,
		"dynamicValues": [],
		"customAttributes": {"id_element": "job_container"},
	}

	return block


def _inject_jobs_into_block(block, jobs):
	"""
	Recursively walk *block* (and all descendants via "children").
	When a block whose customAttributes.id_block == "job_openings" is found,
	replace its children with newly generated job card blocks and update baseStyles.

	Returns True if the target container was found (and updated).
	"""
	custom_attrs = block.get("customAttributes") or {}
	if custom_attrs.get("id_block") == "job_openings":
		block["children"] = [_build_job_block(job) for job in jobs]
		block["baseStyles"] = {
			"display": "grid",
			"flexDirection": "column",
			"flexShrink": 0,
			"gap": "20px",
			"gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
			"height": "fit-content",
			"overflow": "hidden",
			"padding": "20px",
			"position": "static",
			"width": "100%",
			"gridAutoColumns": "minmax(0, 1fr)",
			"marginBottom": "109px",
		}
		return True

	for child in block.get("children") or []:
		if _inject_jobs_into_block(child, jobs):
			return True

	return False


@frappe.whitelist(allow_guest=True)
def inject_job_openings(id_page, jobs):
	"""
	Insert job-opening card blocks into the container that has
	customAttributes.id_block == "job_openings" inside a Builder Page.

	:param id_page: Name (ID) of the Builder Page doctype record.
	:param jobs:    JSON string or list of job dicts, each containing:
	                  job_title, job_typework, job_location,
	                  job_deadline, job_salary, link_job
	"""
	# --- normalise jobs argument ---
	if isinstance(jobs, str):
		jobs = json.loads(jobs)

	# --- fetch the page record ---
	page_doc = frappe.get_doc("Builder Page", id_page)

	# blocks is stored as a JSON string in the doctype
	blocks = page_doc.blocks
	if isinstance(blocks, str):
		blocks = json.loads(blocks)

	if not isinstance(blocks, list):
		frappe.throw(f"Unexpected blocks format for page '{id_page}'.")

	# --- walk the block tree and inject ---
	found = False
	for block in blocks:
		if _inject_jobs_into_block(block, jobs):
			found = True
			break

	if not found:
		frappe.throw(
			"Không tìm thấy container có id_block='job_openings' trong trang này."
		)

	# --- persist ---
	page_doc.blocks = json.dumps(blocks, ensure_ascii=False)
	page_doc.draft_blocks = json.dumps(blocks, ensure_ascii=False)
	page_doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {"message": "Đã chèn thành công các tin tuyển dụng vào trang.", "total": len(jobs)}


# ---------------------------------------------------------------------------
# Dữ liệu mẫu – 10 vị trí tuyển dụng dùng để kiểm thử
# ---------------------------------------------------------------------------

SAMPLE_JOBS = [
	{
		"job_title": "Kỹ sư Phần mềm Backend",
		"job_typework": "Toàn thời gian",
		"job_location": "Hà Nội",
		"job_deadline": "31/07/2026",
		"job_salary": "20.000.000 – 35.000.000 VNĐ",
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-42dc8a52",
	},
	{
		"job_title": "Kỹ sư Phần mềm Frontend",
		"job_typework": "Toàn thời gian",
		"job_location": "Hồ Chí Minh",
		"job_deadline": "31/07/2026",
		"job_salary": "18.000.000 – 30.000.000 VNĐ",
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-bcd816c7",
	},
	{
		"job_title": "Chuyên viên Thiết kế UI/UX",
		"job_typework": "Toàn thời gian",
		"job_location": "Hà Nội",
		"job_deadline": "15/08/2026",
		"job_salary": None,
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-279c682f",
	},
	{
		"job_title": "Product Manager",
		"job_typework": "Toàn thời gian",
		"job_location": "Hồ Chí Minh",
		"job_deadline": "30/08/2026",
		"job_salary": "30.000.000 – 50.000.000 VNĐ",
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-e2d5c635",
	},
	{
		"job_title": "Data Analyst",
		"job_typework": "Toàn thời gian",
		"job_location": "Đà Nẵng",
		"job_deadline": "20/08/2026",
		"job_salary": "15.000.000 – 25.000.000 VNĐ",
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-42dc8a52",
	},
	{
		"job_title": "Chuyên viên Marketing Digital",
		"job_typework": "Toàn thời gian",
		"job_location": "Hà Nội",
		"job_deadline": "10/08/2026",
		"job_salary": None,
		"link_job": "http://agent_mbw_cloud.ts:8895/pages/page-bcd816c7",
	},
	{
		"job_title": "Thực tập sinh Truyền thông nội bộ",
		"job_typework": "Thực tập",
		"job_location": "Hà Nội",
		"job_deadline": "10/07/2026",
		"job_salary": None,
		"link_job": "https://example.com/jobs/intern-comms",
	},
	{
		"job_title": "DevOps Engineer",
		"job_typework": "Toàn thời gian",
		"job_location": "Hồ Chí Minh",
		"job_deadline": "05/09/2026",
		"job_salary": "25.000.000 – 45.000.000 VNĐ",
		"link_job": "https://example.com/jobs/devops-engineer",
	},
	{
		"job_title": "Chuyên viên Kinh doanh B2B",
		"job_typework": "Toàn thời gian",
		"job_location": "Hà Nội",
		"job_deadline": "25/08/2026",
		"job_salary": "12.000.000 – 20.000.000 VNĐ + Hoa hồng",
		"link_job": "https://example.com/jobs/b2b-sales",
	},
	{
		"job_title": "QA Engineer (Automation)",
		"job_typework": "Toàn thời gian",
		"job_location": "Hà Nội",
		"job_deadline": "01/09/2026",
		"job_salary": "15.000.000 – 28.000.000 VNĐ",
		"link_job": "https://example.com/jobs/qa-automation",
	},
]


@frappe.whitelist(allow_guest=True)
def inject_sample_job_openings(id_page):
	"""
	Endpoint kiểm thử: chèn 10 tin tuyển dụng mẫu vào trang Builder Page
	có container id_block='job_openings'.

	Gọi:
	  GET/POST /api/method/builder.api_page.page.inject_sample_job_openings?id_page=<page-name>
	"""
	return inject_job_openings(id_page=id_page, jobs=SAMPLE_JOBS)
