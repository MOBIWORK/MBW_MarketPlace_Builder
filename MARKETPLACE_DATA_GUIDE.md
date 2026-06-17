# Hướng dẫn thêm dữ liệu vào DocTypes

Tài liệu này hướng dẫn cách nhập liệu vào 3 DocType chính phục vụ cho marketplace mẫu website: **Builder Website Category**, **Builder Website**, và **Builder Website SEO**. Hỗ trợ cả 2 cách: thao tác trực tiếp trên giao diện Frappe Desk và nhập qua Python/API.

---

## 1. Builder Website Category (Danh mục)

> Cần tạo danh mục **trước tiên**, vì Builder Website cần liên kết đến danh mục.

### Cấu trúc trường

| Trường | Fieldname | Kiểu | Bắt buộc | Mô tả |
| :--- | :--- | :--- | :---: | :--- |
| Category Name | `category_name` | Data | ✅ | Tên hiển thị của danh mục (cũng là Title Field) |
| Description | `description` | Small Text | ❌ | Mô tả ngắn về danh mục |

> **Lưu ý:** Trường `name` (ID document) sẽ được Frappe tự sinh từ `category_name`.

---

### Cách 1: Thêm qua giao diện Frappe Desk

1. Vào **Frappe Desk** → Thanh tìm kiếm → Gõ `Builder Website Category` → Chọn **New**.
2. Điền các trường:
   - **Category Name**: Ví dụ `E-commerce`
   - **Description**: Ví dụ `Mẫu dành cho website bán hàng trực tuyến`
3. Nhấn **Save**.

---

## 2. Builder Website (Mẫu Website)

> Đảm bảo đã có **Builder Website Category** và **Builder Page** (nếu muốn liên kết trang) trước khi tạo.

### Cấu trúc trường

| Trường | Fieldname | Kiểu | Bắt buộc | Mô tả |
| :--- | :--- | :--- | :---: | :--- |
| Title | `title` | Data | ✅ | Tên hiển thị của mẫu website |
| Description | `description` | Small Text | ❌ | Mô tả ngắn về mẫu |
| Thumbnail | `thumbnail` | Attach Image | ❌ | Ảnh đại diện của mẫu |
| Category | `category` | Link → Builder Website Category | ❌ | Danh mục phân loại |
| Logo | `logo` | Attach | ❌ | File logo của website |
| Favicon | `favicon` | Attach | ❌ | File favicon (`.ico`, 16x16px) |
| Status | `status` | Select | ❌ | `draft` hoặc `published` |
| Domain | `domain` | Data | ❌ | Tên miền demo của mẫu |
| Pages | `pages` | Table (Builder Website Page Item) | ❌ | Danh sách các trang của mẫu |

#### Cấu trúc con: Builder Website Page Item (trong bảng `pages`)

| Trường | Fieldname | Kiểu | Mô tả |
| :--- | :--- | :--- | :--- |
| Page Name | `page_name` | Data | Tên trang (ví dụ: `Trang chủ`) |
| Builder Page | `builder_page` | Link → Builder Page | Liên kết đến thiết kế page thực tế |
| Order | `order` | Int | Thứ tự hiển thị (số nhỏ = ưu tiên cao) |
| Is Homepage | `is_homepage` | Check | Đánh dấu đây là trang chủ |
| Status | `status` | Select | `draft` hoặc `published` |
| Is Blog Detail | `is_blog_detail` | Check | Đây là trang chi tiết bài blog |
| Is Blog List | `is_blog_list` | Check | Đây là trang danh sách blog |

---

### Cách 1: Thêm qua giao diện Frappe Desk

1. Vào **Frappe Desk** → Tìm `Builder Website` → Chọn **New**.
2. Điền các trường chính:
   - **Title**: `Mẫu Bán Hàng Cơ Bản`
   - **Description**: `Giao diện hiện đại cho shop bán hàng online`
   - **Thumbnail**: Upload ảnh đại diện
   - **Category**: Chọn danh mục đã tạo (ví dụ: `E-commerce`)
   - **Status**: Chọn `published`
3. Trong bảng **Pages**, thêm các dòng:
   - **Page Name**: `Trang chủ` | **Builder Page**: Chọn page đã thiết kế | **Is Homepage**: ✅ | **Order**: `1`
   - **Page Name**: `Giới thiệu` | **Builder Page**: Chọn page | **Order**: `2`
4. Nhấn **Save**.

---

## 3. Builder Website SEO

> Tạo sau khi đã có **Builder Website**. Mỗi website chỉ nên có **1 bản ghi SEO**.

### Cấu trúc trường

| Trường | Fieldname | Kiểu | Bắt buộc | Mô tả |
| :--- | :--- | :--- | :---: | :--- |
| Website | `website` | Link → Builder Website | ✅ | Website cần cấu hình SEO |
| Meta Title | `meta_title` | Data | ❌ | Tiêu đề hiển thị trên tab trình duyệt và kết quả tìm kiếm |
| Meta Description | `meta_description` | Small Text | ❌ | Mô tả ngắn cho công cụ tìm kiếm (khuyến khích ≤ 160 ký tự) |
| Keywords | `keywords` | JSON | ❌ | Mảng từ khóa, ví dụ `["shop", "mua sắm", "thời trang"]` |
| OG Title | `og_title` | Data | ❌ | Tiêu đề khi chia sẻ lên mạng xã hội |
| OG Description | `og_description` | Small Text | ❌ | Mô tả khi chia sẻ lên mạng xã hội |
| OG Image | `og_image` | Attach Image | ❌ | Ảnh preview khi chia sẻ (khuyến khích 1200x630px) |
| Robots | `robots` | Attach | ❌ | File `robots.txt` |
| Sitemap Enabled | `sitemap_enabled` | Check | ❌ | Bật/tắt sitemap |

---

### Cách 1: Thêm qua giao diện Frappe Desk

1. Vào **Frappe Desk** → Tìm `Builder Website SEO` → Chọn **New**.
2. Điền các trường:
   - **Website**: Chọn website vừa tạo (ví dụ: `Mẫu Bán Hàng Cơ Bản`)
   - **Meta Title**: `Mua sắm online - Mẫu Bán Hàng Cơ Bản`
   - **Meta Description**: `Khám phá hàng ngàn sản phẩm chất lượng...`
   - **Keywords**: `["shop", "mua sắm", "online", "thời trang"]`
   - **OG Title**: `Mua sắm tuyệt vời cùng chúng tôi`
   - **OG Image**: Upload ảnh preview
   - **Sitemap Enabled**: ✅
3. Nhấn **Save**.

---

## Thứ tự nhập liệu khuyến nghị

```
1. Builder Website Category   →  Tạo các danh mục phân loại
2. Builder Page               →  Thiết kế giao diện từng trang trong app Builder
3. Builder Website            →  Tạo mẫu website, liên kết page và category
4. Builder Website SEO        →  Thêm cấu hình SEO cho từng mẫu website
```
