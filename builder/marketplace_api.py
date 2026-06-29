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
