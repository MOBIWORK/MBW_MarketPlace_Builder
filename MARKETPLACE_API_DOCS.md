# Hướng dẫn sử dụng Builder Marketplace APIs

Tài liệu này hướng dẫn cách sử dụng 3 API được cung cấp để tương tác với kho mẫu giao diện (Templates) của ứng dụng Builder. Các API này được phép gọi mà **không cần yêu cầu đăng nhập (Guest Access)**, rất phù hợp cho việc tích hợp vào trang web hoặc ứng dụng bên ngoài.

---

## 1. Lấy danh sách mẫu Website (Templates)

Lấy ra danh sách các mẫu website đang ở trạng thái `published`. Hỗ trợ phân trang và lọc theo danh mục.

**Endpoint:**
```http
GET/POST /api/method/builder.marketplace_api.get_website_templates
```

**Tham số:**
| Tên | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | Không | `30` | Số lượng bản ghi muốn lấy |
| `start` | `int` | Không | `0` | Vị trí bắt đầu lấy (dùng để phân trang) |
| `category` | `string` | Không | `null` | Tên ID của danh mục cần lọc (ví dụ: `E-commerce`) |

**Ví dụ Request:**
```bash
curl -X GET "https://your-domain.com/api/method/builder.marketplace_api.get_website_templates?limit=10&start=0"
```

**Ví dụ Response:**
```json
{
    "message": {
        "data": [
            {
                "name": "Template-001",
                "title": "Mẫu Bán Hàng Cơ Bản",
                "description": "Mẫu giao diện dành cho shop bán hàng",
                "thumbnail": "/files/thumb1.jpg",
                "category": "E-commerce"
            }
        ],
        "total_count": 15
    }
}
```

---

## 2. Lấy chi tiết mẫu Website (Website Detail)

Truy xuất toàn bộ dữ liệu của một mẫu website theo `website_id`, bao gồm cấu hình cơ bản, danh sách các trang (pages) với chi tiết thiết kế block (json), và thông tin SEO.

**Endpoint:**
```http
GET/POST /api/method/builder.marketplace_api.get_website_detail
```

**Tham số:**
| Tên | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `website_id` | `string` | Có | - | Mã ID (name) của Builder Website |

**Ví dụ Request:**
```bash
curl -X GET "https://your-domain.com/api/method/builder.marketplace_api.get_website_detail?website_id=Template-001"
```

**Ví dụ Response:**
```json
{
    "message": {
        "website_info": {
            "name": "Template-001",
            "title": "Mẫu Bán Hàng Cơ Bản",
            "description": "...",
            "thumbnail": "/files/thumb1.jpg",
            "category": "E-commerce",
            "logo": "/files/logo.png",
            "favicon": "/files/favicon.ico",
            "status": "published",
            "domain": "shop.example.com"
        },
        "pages": [
            {
                "page_name": "Trang chủ",
                "builder_page": "page-281b3x",
                "order": 1,
                "is_homepage": 1,
                "status": "published",
                "is_blog_detail": 0,
                "is_blog_list": 0,
                "blocks": [
                    {
                        "id": "block-uuid",
                        "tag": "div",
                        "content": "Chào mừng..."
                    }
                ],
                "draft_blocks": null
            }
        ],
        "seo_info": {
            "meta_title": "Mua sắm tuyệt vời",
            "meta_description": "Trang bán hàng trực tuyến...",
            "keywords": ["shop", "online"],
            "og_title": "Mua sắm tuyệt vời",
            "og_description": "...",
            "og_image": "/files/og-image.jpg",
            "robots": "",
            "sitemap_enabled": 1
        }
    }
}
```

---

## 3. Lấy danh sách danh mục (Categories)

Lấy ra danh sách tất cả các danh mục để phục vụ hiển thị menu lọc mẫu website. Hỗ trợ phân trang.

**Endpoint:**
```http
GET/POST /api/method/builder.marketplace_api.get_website_categories
```

**Tham số:**
| Tên | Kiểu | Bắt buộc | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `limit` | `int` | Không | `100` | Số lượng bản ghi muốn lấy |
| `start` | `int` | Không | `0` | Vị trí bắt đầu lấy (dùng để phân trang) |

**Ví dụ Request:**
```bash
curl -X GET "https://your-domain.com/api/method/builder.marketplace_api.get_website_categories"
```

**Ví dụ Response:**
```json
{
    "message": {
        "data": [
            {
                "name": "E-commerce",
                "category_name": "E-commerce",
                "description": "Các mẫu dành cho bán hàng trực tuyến"
            },
            {
                "name": "Blog",
                "category_name": "Blog",
                "description": "Mẫu blog cá nhân, tin tức"
            }
        ],
        "total_count": 5
    }
}
```
