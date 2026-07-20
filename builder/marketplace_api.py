"""
Marketplace API for Builder Website Templates.

This file provides read-only endpoints for listing and retrieving website
templates, their associated pages/blocks, SEO settings and categories.
It lives alongside the core app but does not modify any core files, making
upstream merges conflict-free.
"""

import frappe


@frappe.whitelist(allow_guest=True)
def get_website_templates(limit=30, start=0, category=None):
    """Return a paginated list of published website templates.

    Args:
        limit (int): Number of records to fetch. Default 30.
        start (int): Offset for pagination. Default 0.
        category (str | None): Filter by Builder Website Category name.

    Returns:
        dict: {data: [...], total_count: int}
    """
    filters = {"status": "published"}
    if category:
        filters["category"] = category

    data = frappe.get_all(
        "Builder Website",
        filters=filters,
        fields=["name", "title", "description", "thumbnail", "category", "preview_url"],
        limit=int(limit),
        start=int(start),
        order_by="modified desc",
    )

    for row in data:
        row["thumbnail"] = _absolute_url(row.get("thumbnail"))

    total_count = frappe.db.count("Builder Website", filters=filters)

    return {"data": data, "total_count": total_count}


@frappe.whitelist(allow_guest=True)
def get_website_detail(website_id):
    """Return full detail of a website template including pages, blocks and SEO.

    Fetches:
    - Builder Website (main info)
    - Builder Website Page Item (child table rows, ordered by `order`)
    - Builder Page (blocks) for each page item
    - Builder Website SEO linked to this website

    Args:
        website_id (str): The `name` (ID) of the Builder Website document.

    Returns:
        dict: {website_info, pages, seo_info}
    """
    if not website_id:
        frappe.throw("Tham số 'website_id' là bắt buộc.", frappe.MandatoryError)

    website = frappe.get_doc("Builder Website", website_id)

    website_info = {
        "name": website.name,
        "title": website.title,
        "description": website.description,
        "thumbnail": _absolute_url(website.thumbnail),
        "category": website.category,
        "logo": _absolute_url(website.logo),
        "favicon": _absolute_url(website.favicon),
        "status": website.status,
        "domain": website.domain,
    }

    pages = _build_pages_list(website.pages)

    seo_info = _fetch_seo(website_id)

    return {"website_info": website_info, "pages": pages, "seo_info": seo_info}


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_website_content_brief(website_id):
    """Return the content brief (AI generation spec) of a website template.

    Unlike ``get_website_detail`` (which returns rendered blocks), this returns
    only the editorial intent: who the site targets, what it should convert,
    the content angle, and the per-page section outline. It is the input an AI
    service needs to generate copy for the template.

    Args:
        website_id (str): The `name` (ID) of the Builder Website document.

    Returns:
        dict: {template_id, target_audience, conversion_goal, content_angle,
        pages: [{slug, title, purpose, sections}]}
    """
    if not website_id:
        frappe.throw("Tham số 'website_id' là bắt buộc.", frappe.MandatoryError)

    website = frappe.get_doc("Builder Website", website_id)

    return {
        "template_id": website.name,
        "target_audience": website.target_audience,
        "conversion_goal": website.conversion_goal,
        "content_angle": website.content_angle,
        "pages": _build_content_brief_pages(website.pages),
    }


@frappe.whitelist(allow_guest=True)
def get_website_categories(limit=100, start=0):
    """Return a paginated list of website categories.

    Args:
        limit (int): Number of records to fetch. Default 100.
        start (int): Offset for pagination. Default 0.

    Returns:
        dict: {data: [...], total_count: int}
    """
    data = frappe.get_all(
        "Builder Website Category",
        fields=["name", "category_name", "description"],
        limit=int(limit),
        start=int(start),
        order_by="category_name asc",
    )

    total_count = frappe.db.count("Builder Website Category")

    return {"data": data, "total_count": total_count}


@frappe.whitelist(allow_guest=True)
def get_builder_variables():
    """Return the full list of Builder Variable records (global design tokens).

    Builder Variable is not linked to a specific website; the records form a
    shared list of design tokens (colors and dimensions). This endpoint is
    intended for the AI service, which needs the complete set at once, so it
    returns every record with no pagination.

    Returns:
        dict: {data: [...], total_count: int}
    """
    data = _fetch_variables()

    return {"data": data, "total_count": len(data)}


# Template field -> Builder Page field. Khi trường của Template trống thì lấy
# giá trị tương ứng từ Builder Page được liên kết qua `builder_page`.
TEMPLATE_FALLBACK_FIELDS = {
    "title": "page_title",
    "thumbnail": "preview",
    "description": "meta_description",
}


@frappe.whitelist(allow_guest=True)
def get_page_templates(limit=30, start=0, title=None, industry="All", purpose=None):
    """Return a paginated list of single-page templates with optional filters.

    Unlike ``get_website_templates`` (which lists multi-page Builder Website
    templates), this lists ``Template`` records — templates for a single page.

    Args:
        limit (int): Number of records to fetch. Default 30.
        start (int): Offset for pagination. Default 0.
        title (str | None): Filter by title (partial match).
        industry (str): Filter by Template Industry name. "All" (default)
            fetches every industry.
        purpose (str | None): Filter by purpose (Recruitment / Marketing /
            Website).

    Returns:
        dict: {data: [...], total_count: int}. For each template, any empty
        field listed in TEMPLATE_FALLBACK_FIELDS is filled from the linked
        Builder Page.
    """
    filters = {}
    if title:
        filters["title"] = ["like", f"%{title}%"]
    if industry and industry != "All":
        filters["industry"] = industry
    if purpose:
        filters["purpose"] = purpose

    data = frappe.get_all(
        "Template",
        filters=filters,
        fields=[
            "name",
            "title",
            "builder_page",
            "purpose",
            "industry",
            "thumbnail",
            "description",
            "status",
            "is_featured",
            "is_homepage",
            "is_blog_detail",
            "is_blog_list",
            "is_job_list",
            "is_job_detail",
            "sort_order",
        ],
        limit=int(limit),
        start=int(start),
        order_by="sort_order asc, modified desc",
    )

    _apply_builder_page_fallback(data)

    for row in data:
        row["thumbnail"] = _absolute_url(row.get("thumbnail"))

    total_count = frappe.db.count("Template", filters=filters)

    return {"data": data, "total_count": total_count}


@frappe.whitelist(allow_guest=True)
def get_page_template_industries(purpose=None):
    """Return the list of enabled template industries, optionally by purpose.

    Args:
        purpose (str | None): Filter by purpose (Recruitment / Marketing /
            Website). Empty or "All" fetches every industry.

    Returns:
        dict: {data: [...], total_count: int}, ordered by sort_order.
    """
    filters = {"enabled": 1}
    if purpose and purpose != "All":
        filters["purpose"] = purpose

    data = frappe.get_all(
        "Template Industry",
        filters=filters,
        fields=["name", "title", "purpose", "icon", "description", "sort_order"],
        order_by="sort_order asc, title asc",
    )

    for row in data:
        row["icon"] = _absolute_url(row.get("icon"))

    total_count = frappe.db.count("Template Industry", filters=filters)

    return {"data": data, "total_count": total_count}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _absolute_url(path):
    """Convert a stored file path to an absolute URL.

    Builder stores attachments as site-relative paths (e.g.
    ``files/thumbnail.jpeg`` or ``/files/thumbnail.jpeg``). These cannot be
    resolved by an external consumer, so prepend the site URL. Values that are
    already absolute (http/https) or empty are returned unchanged.

    Args:
        path (str | None): Stored file path.

    Returns:
        str | None: Absolute URL or the original value if empty/absolute.
    """
    if not path or path.startswith(("http://", "https://", "//")):
        return path
    return frappe.utils.get_url(path if path.startswith("/") else f"/{path}")


def _apply_builder_page_fallback(templates):
    """Fill empty template fields from the linked Builder Page.

    For each template with a `builder_page`, any field listed in
    TEMPLATE_FALLBACK_FIELDS that is empty gets the corresponding value from
    the Builder Page. Builder Pages are fetched in a single query to avoid an
    N+1 lookup.

    Args:
        templates (list[dict]): rows to mutate in place.
    """
    page_names = list({t["builder_page"] for t in templates if t.get("builder_page")})
    if not page_names:
        return

    pages = frappe.get_all(
        "Builder Page",
        filters={"name": ["in", page_names]},
        fields=["name", *TEMPLATE_FALLBACK_FIELDS.values()],
    )
    page_map = {p["name"]: p for p in pages}

    for template in templates:
        page = page_map.get(template.get("builder_page"))
        if not page:
            continue
        for tpl_field, page_field in TEMPLATE_FALLBACK_FIELDS.items():
            if not template.get(tpl_field):
                template[tpl_field] = page.get(page_field)


def _build_pages_list(page_items):
    """Build a list of page dicts from Builder Website Page Item rows.

    For each item that has a linked `builder_page`, the corresponding
    Builder Page document's `blocks` and `draft_blocks` fields are fetched
    and embedded in the result.

    Args:
        page_items (list): child table rows from Builder Website.pages

    Returns:
        list[dict]
    """
    pages = []
    for item in sorted(page_items, key=lambda x: x.order or 0):
        builder_page_info = frappe.get_doc("Builder Page", item.builder_page)
        page_data = {
            "page_name": item.page_name,
            "builder_page": item.builder_page,
            "order": item.order,
            "is_homepage": item.is_homepage,
            "status": item.status,
            "is_blog_detail": item.is_blog_detail,
            "is_blog_list": item.is_blog_list,
            "blocks": None,
            "draft_blocks": None,
            "is_job_list": item.is_job_list,
            "is_job_detail": item.is_job_detail,
            "page_data_script": builder_page_info.page_data_script,
            "head_html": builder_page_info.head_html,
            "body_html": builder_page_info.body_html
        }

        if item.builder_page:
            page_data.update(_fetch_builder_page_blocks(item.builder_page))

        pages.append(page_data)

    return pages


def _build_content_brief_pages(page_items):
    """Build the `pages` outline of a content brief from child table rows.

    The slug of each page comes from the linked Builder Page's `route`; the
    routes are fetched in a single query to avoid an N+1 lookup. Rows are
    ordered by `order` and their `sections_page` JSON is parsed so consumers
    get real objects instead of a string.

    Args:
        page_items (list): child table rows from Builder Website.pages

    Returns:
        list[dict]: [{slug, title, purpose, sections}]
    """
    page_names = list({i.builder_page for i in page_items if i.builder_page})
    route_map = {}
    if page_names:
        route_map = {
            p["name"]: p["route"]
            for p in frappe.get_all(
                "Builder Page",
                filters={"name": ["in", page_names]},
                fields=["name", "route"],
            )
        }

    pages = []
    for item in sorted(page_items, key=lambda x: x.order or 0):
        pages.append(
            {
                "slug": _to_slug(route_map.get(item.builder_page), item.is_homepage),
                "title": item.page_name,
                "purpose": item.purpose,
                "sections": frappe.parse_json(item.sections_page) if item.sections_page else [],
            }
        )

    return pages


def _to_slug(route, is_homepage=False):
    """Normalise a Builder Page route into a leading-slash slug.

    Builder stores routes without a leading slash (e.g. ``about``) and the
    homepage may have an empty route. The brief expects ``/about`` and ``/``.

    Args:
        route (str | None): Stored Builder Page route.
        is_homepage (bool): Whether the page item is flagged as the homepage.

    Returns:
        str: Slug beginning with "/".
    """
    if not route:
        return "/" if is_homepage else None
    return route if route.startswith("/") else f"/{route}"


def _fetch_builder_page_blocks(builder_page_name):
    """Fetch blocks and draft_blocks from a Builder Page document.

    Args:
        builder_page_name (str): The name/ID of the Builder Page.

    Returns:
        dict: {blocks, draft_blocks}
    """
    doc = frappe.get_doc("Builder Page", builder_page_name)
    return {
        "blocks": frappe.parse_json(doc.blocks) if doc.blocks else None,
        "draft_blocks": frappe.parse_json(doc.draft_blocks) if doc.draft_blocks else None,
    }


def _fetch_variables():
    """Fetch all Builder Variable records (global design tokens).

    Builder Variable is not linked to a specific website; the records form a
    shared list of design tokens (colors and dimensions) consumed by templates.

    Returns:
        list[dict]
    """
    return frappe.get_all(
        "Builder Variable",
        fields=["name", "variable_name", "group", "type", "value", "dark_value", "is_standard"],
        order_by="`group` asc, variable_name asc",
    )


def _fetch_seo(website_id):
    """Fetch the Builder Website SEO record linked to a website.

    Args:
        website_id (str): Builder Website name.

    Returns:
        dict | None: SEO data or None if not found.
    """
    seo_name = frappe.db.get_value("Builder Website SEO", {"website": website_id}, "name")
    if not seo_name:
        return None

    doc = frappe.get_doc("Builder Website SEO", seo_name)
    return {
        "meta_title": doc.meta_title,
        "meta_description": doc.meta_description,
        "keywords": frappe.parse_json(doc.keywords) if doc.keywords else None,
        "og_title": doc.og_title,
        "og_description": doc.og_description,
        "og_image": _absolute_url(doc.og_image),
        "robots": doc.robots,
        "sitemap_enabled": doc.sitemap_enabled,
    }
