# 📖 GIẢI THÍCH ĐƠN GIẢN VỀ DỰ ÁN

## 🎯 Dự án làm gì?

Tưởng tượng bạn muốn biết **lương IT ở Việt Nam là bao nhiêu**, bạn phải lên TopCV search từng công việc một rồi note lại rất mất thời gian.

Dự án này **tự động làm việc đó** cho bạn:
1. Thu thập thông tin việc làm từ TopCV
2. Xử lý và tính toán mức lương
3. Hiển thị ra biểu đồ, bảng đẹp mắt

---

## 🗂️ CÁC THÀNH PHẦN CHÍNH

Dự án gồm **4 phần lớn**:

```
📁 src/                    → Code thu thập và xử lý dữ liệu
📁 backend/                → Máy chủ cung cấp dữ liệu
📁 frontend/               → Giao diện người dùng
📁 data/                   → Nơi lưu dữ liệu
```

---

## 📂 PHẦN 1: THU THẬP DỮ LIỆU (src/)

### 📄 File: `src/crawler/topcv_crawler.py`

**Nhiệm vụ**: Vào website TopCV và lấy thông tin việc làm

**Hoạt động như thế nào?**

1. Mở trình duyệt ảo (không thấy cửa sổ)
2. Vào trang TopCV tìm kiếm việc làm IT
3. Đọc từng tin tuyển dụng và lấy:
   - Tên công việc (VD: "Senior Python Developer")
   - Tên công ty (VD: "VNG Corporation")
   - Địa điểm (VD: "Ho Chi Minh")
   - Mức lương (VD: "15-20 triệu")
   - Cấp độ (VD: "Senior")
   - Link chi tiết
4. Lưu tất cả vào file Excel (CSV)

**Kết quả**: File `data/raw/topcv_jobs_20260130.csv` chứa dữ liệu thô

**Ví dụ dữ liệu thô**:
```
title                       | company  | salary        | location     | level
Senior Python Developer     | VNG      | 15-20 triệu   | Ho Chi Minh  | Senior
Junior Frontend Developer   | Tiki     | 8-12 triệu    | Ha Noi       | Junior
```

---

### 📄 File: `src/processing/salary_parser.py`

**Nhiệm vụ**: Đọc file Excel thô và làm sạch dữ liệu

**Vấn đề**: Mức lương viết lung tung:
- "15-20 triệu"
- "Lên đến 30 triệu"
- "Từ 2000 USD"
- "Thỏa thuận"
- "10-15tr/tháng"

**Giải pháp**: File này sẽ đọc và chuyển tất cả về dạng số chuẩn

**Ví dụ xử lý**:
```
"15-20 triệu"      → Lương trung bình: 17.5 triệu
"Lên đến 30 triệu" → Lương trung bình: 30 triệu
"Từ 2000 USD"      → Chuyển sang VND: 50 triệu
"Thỏa thuận"       → Để trống (NULL)
```

**Kết quả**: File `data/processed/processed_topcv_jobs_20260130.csv` (dữ liệu sạch)

**Ví dụ dữ liệu sạch**:
```
title                       | company  | avg_salary_mil_vnd | location     | level
Senior Python Developer     | VNG      | 17.5               | Ho Chi Minh  | Senior
Junior Frontend Developer   | Tiki     | 10.0               | Ha Noi       | Junior
```

---

### 📄 File: `generate_diverse_data.py`

**Nhiệm vụ**: Tạo dữ liệu mẫu đa dạng để demo

**Tại sao cần?** Vì TopCV nhiều công việc không có lương rõ ràng (ghi "Thỏa thuận")

**Làm gì?**
- Tạo 45 công việc giả lập nhưng realistic
- Bao gồm nhiều công ty: VNG, Tiki, FPT, Shopee, Grab...
- Nhiều cấp độ: Junior, Mid-level, Senior, Lead, Manager
- Nhiều địa điểm: HCM, Hà Nội, Đà Nẵng, Remote
- Lương phù hợp với thị trường (7-200 triệu)

**Kết quả**: File CSV với 45 jobs đầy đủ thông tin

---

### 📄 File: `import_to_db.py`

**Nhiệm vụ**: Đưa dữ liệu từ file Excel vào Database

**Hoạt động**:
1. Đọc file CSV đã xử lý
2. Mở database SQLite (file `data/jobs.db`)
3. Xóa dữ liệu cũ (nếu có)
4. Chép 45 jobs vào database

**Tại sao cần database?** 
- File Excel: Khó tìm kiếm, lọc dữ liệu
- Database: Tìm kiếm nhanh, lọc linh hoạt

---

## 📂 PHẦN 2: MÁY CHỦ BACKEND (backend/)

### 📄 File: `backend/models.py`

**Nhiệm vụ**: Định nghĩa cấu trúc dữ liệu trong database

**Giải thích đơn giản**: Giống như tạo bảng trong Excel với các cột

**Bảng "jobs" có các cột**:
- `id`: Số thứ tự (1, 2, 3...)
- `title`: Tên công việc
- `company`: Tên công ty
- `level`: Cấp độ (Junior/Mid/Senior/Lead/Manager)
- `location`: Địa điểm (HCM, Hà Nội...)
- `avg_salary_mil_vnd`: Lương trung bình (triệu VND)
- `skills`: Kỹ năng cần (Python, React, Java...)
- `url`: Link chi tiết

**Ví dụ 1 record**:
```
id: 1
title: Senior Backend Developer
company: VNG Corporation
level: Senior
location: Ho Chi Minh
avg_salary_mil_vnd: 55.0
skills: Python, FastAPI, PostgreSQL
```

---

### 📄 File: `backend/database.py`

**Nhiệm vụ**: Kết nối đến database SQLite

**Giải thích đơn giản**: 
- Mở file `data/jobs.db` 
- Tạo "cầu nối" để các file khác truy cập database

---

### 📄 File: `backend/crud.py`

**Nhiệm vụ**: Các hàm để đọc/ghi dữ liệu từ database

**CRUD là gì?**
- **C**reate: Tạo mới (thêm job)
- **R**ead: Đọc dữ liệu (lấy danh sách jobs)
- **U**pdate: Cập nhật (sửa thông tin job)
- **D**elete: Xóa (xóa job)

**Các hàm chính**:

1. **`get_jobs()`** - Lấy danh sách công việc
   - Có thể lọc theo: tên, công ty, địa điểm, lương
   - Có thể sắp xếp
   - Có phân trang (page 1, 2, 3...)

2. **`get_job(id)`** - Lấy chi tiết 1 công việc

3. **`avg_by_location()`** - Tính lương trung bình theo địa điểm
   - VD: HCM: 46 triệu, Hà Nội: 42 triệu

4. **`avg_by_level()`** - Tính lương trung bình theo cấp độ
   - VD: Senior: 55 triệu, Mid: 35 triệu, Junior: 12 triệu

5. **`salary_distribution()`** - Lấy tất cả mức lương để vẽ biểu đồ

6. **`top_skills()`** - Đếm xem skill nào được yêu cầu nhiều nhất

---

### 📄 File: `backend/schemas.py`

**Nhiệm vụ**: Định nghĩa format dữ liệu khi gửi/nhận qua mạng

**Giải thích đơn giản**: 
- Quy định rõ ràng: Gửi/nhận dữ liệu kiểu gì
- Kiểm tra dữ liệu có đúng format không

**Ví dụ**:
- `JobOut`: Format khi trả job về frontend
- `JobCreate`: Format khi tạo job mới
- `UserLogin`: Format khi đăng nhập

---

### 📄 File: `backend/main.py` ⭐ (FILE QUAN TRỌNG NHẤT)

**Nhiệm vụ**: Máy chủ web - "Trái tim" của backend

**Hoạt động**: Lắng nghe các yêu cầu từ frontend và trả về dữ liệu

**Các "đường đi" (endpoints)**:

#### 🔹 Nhóm 1: Lấy danh sách công việc

**`GET /api/jobs`** - Lấy danh sách jobs
- Frontend gửi: "Cho tôi jobs ở HCM, lương 30-50 triệu, trang 1"
- Backend trả về: Danh sách 50 jobs + tổng số jobs

**`GET /api/jobs/5`** - Lấy chi tiết job số 5
- Frontend: "Cho tôi thông tin job ID=5"
- Backend: Trả về đầy đủ thông tin job đó

**`GET /api/metadata`** - Lấy danh sách filters
- Frontend: "Cho tôi danh sách tất cả địa điểm, cấp độ"
- Backend: ["Ho Chi Minh", "Ha Noi", ...], ["Junior", "Senior", ...]

#### 🔹 Nhóm 2: Phân tích dữ liệu

**`GET /api/analytics/salary_distribution`**
- Frontend: "Cho tôi tất cả mức lương để vẽ biểu đồ"
- Backend: [17.5, 20, 25, 30, 35, 40, 45, 50, 55, ...]

**`GET /api/analytics/by_location`**
- Frontend: "Lương trung bình theo địa điểm?"
- Backend: 
  ```
  HCM: 46 triệu (20 jobs)
  Hà Nội: 42 triệu (20 jobs)
  Đà Nẵng: 28.8 triệu (3 jobs)
  ```

**`GET /api/analytics/by_level`**
- Frontend: "Lương trung bình theo cấp độ?"
- Backend:
  ```
  Manager: 110 triệu (4 jobs)
  Lead: 72.5 triệu (3 jobs)
  Senior: 55 triệu (10 jobs)
  Mid-level: 34.7 triệu (17 jobs)
  Junior: 12.4 triệu (11 jobs)
  ```

**`GET /api/analytics/top-skills?limit=15`**
- Frontend: "Top 15 skills được yêu cầu nhiều nhất?"
- Backend:
  ```
  React: 7 jobs
  Java: 7 jobs
  Python: 6 jobs
  JavaScript: 6 jobs
  Node.js: 5 jobs
  ...
  ```

**`GET /api/analytics/company-analysis?limit=12`**
- Frontend: "Top 12 công ty tuyển nhiều nhất?"
- Backend:
  ```
  VNG: 3 jobs, lương TB 60 triệu
  Tiki: 2 jobs, lương TB 45 triệu
  FPT: 2 jobs, lương TB 40 triệu
  ...
  ```

**`GET /api/analytics/top-30-jobs`**
- Frontend: "Top 30 jobs lương cao nhất?"
- Backend: Danh sách 30 jobs được sắp xếp theo lương giảm dần

---

### 📄 File: `backend/auth.py`

**Nhiệm vụ**: Xác thực người dùng (Login/Logout)

**Hoạt động**:
1. Người dùng nhập username + password
2. Check trong database có đúng không
3. Nếu đúng: Tạo "thẻ thông hành" (JWT token)
4. Frontend lưu thẻ này, dùng cho các request sau

---

## 📂 PHẦN 3: GIAO DIỆN FRONTEND (frontend/)

### 📄 File: `frontend/src/App.tsx` ⭐ (FILE CHÍNH)

**Nhiệm vụ**: Giao diện chính của website

**Cấu trúc**: Có 5 tabs (thẻ)

```
┌──────────────────────────────────────────────┐
│  [ Dashboard ] [ Analytics ] [ Search ] ...  │ ← Tabs
├──────────────────────────────────────────────┤
│                                              │
│          Nội dung của tab đang chọn          │
│                                              │
└──────────────────────────────────────────────┘
```

**Hoạt động**:
1. Khi website mở, tự động gọi API lấy dữ liệu
2. Vẽ biểu đồ với dữ liệu nhận được
3. User click tabs → Đổi nội dung hiển thị
4. User tương tác (search, click) → Gọi API lấy dữ liệu mới

---

### 📁 Folder: `frontend/src/components/`

Chứa các **component** - từng phần nhỏ của giao diện

#### 📄 `JobList.tsx`

**Nhiệm vụ**: Hiển thị bảng danh sách công việc

**Chức năng**:
- Hiển thị jobs dạng bảng (table)
- Phân trang (trang 1, 2, 3...)
- Click vào job → Xem chi tiết

**Giao diện**:
```
┌─────────────────────────────────────────────────────────────────┐
│ Title                    | Company | Location  | Level  | Salary │
├─────────────────────────────────────────────────────────────────┤
│ Senior Python Developer  | VNG     | HCM       | Senior | 55     │
│ Junior React Developer   | Tiki    | Ha Noi    | Junior | 12     │
│ ...                                                              │
└─────────────────────────────────────────────────────────────────┘
                    [ 1 ] [ 2 ] [ 3 ] ... ← Pagination
```

---

#### 📄 `AdvancedSearch.tsx`

**Nhiệm vụ**: Form tìm kiếm nâng cao

**Chức năng**:
- Nhiều ô input để lọc:
  - Job title: "python"
  - Company: "VNG"
  - Location: "Ho Chi Minh"
  - Level: "Senior"
  - Salary: 30-50 triệu
- Click "Tìm kiếm" → Gọi API với filters
- Hiển thị kết quả dạng bảng
- Nút "Export Excel" → Download file Excel

**Giao diện**:
```
┌──────────────────────────────────────┐
│  Job Title:     [python          ]  │
│  Company:       [VNG              ]  │
│  Location:      [Ho Chi Minh ▼   ]  │
│  Level:         [Senior       ▼  ]  │
│  Min Salary:    [30              ]  │
│  Max Salary:    [50              ]  │
│                                      │
│      [ 🔍 Tìm kiếm ]  [ 📥 Excel ]   │
└──────────────────────────────────────┘

Results: 5 jobs found
┌────────────────────────────────────────┐
│ Senior Python Developer - VNG - 55tr   │
│ Senior Backend Engineer - Tiki - 45tr  │
│ ...                                    │
└────────────────────────────────────────┘
```

---

#### 📄 `AdvancedAnalytics.tsx`

**Nhiệm vụ**: Tab phân tích nâng cao

**Hiển thị**:
1. **Statistics Cards** (4 thẻ thống kê):
   ```
   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
   │ Total Jobs    │ │ Avg Salary    │ │ Top Location  │ │ Top Skill     │
   │    45         │ │   42 triệu    │ │  Ho Chi Minh  │ │    React      │
   └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
   ```

2. **Top Skills Chart** (Biểu đồ cột):
   ```
   React     ████████ 7
   Java      ████████ 7
   Python    ██████ 6
   JavaScript██████ 6
   Node.js   ████ 5
   ```

3. **Company Analysis** (Biểu đồ tròn):
   - Pie chart hiển thị công ty nào tuyển nhiều

4. **Title-Salary Insights** (Bảng):
   - Job title nào có lương cao nhất

---

#### 📄 `Top30Jobs.tsx`

**Nhiệm vụ**: Hiển thị top 30 jobs lương cao

**Giao diện**: Danh sách các job cards được sắp xếp theo lương

```
┌────────────────────────────────────────────────┐
│ 🥇 #1 - CTO - VNG - 200 triệu/tháng           │
│    Location: Ho Chi Minh | Level: Manager      │
│    Skills: Leadership, Architecture, Cloud     │
├────────────────────────────────────────────────┤
│ 🥈 #2 - Engineering Manager - Grab - 150 triệu│
│    Location: Remote | Level: Manager           │
│    ...                                         │
└────────────────────────────────────────────────┘
```

---

#### 📄 `DataSources.tsx`

**Nhiệm vụ**: Hiển thị thông tin nguồn dữ liệu và trending

**Nội dung**:
- Market Overview: Tổng quan thị trường
- Data Sources: TopCV, ITviec (future)
- Trending Jobs: Công việc hot nhất

---

#### 📄 `AdminPanel.tsx`

**Nhiệm vụ**: Panel quản trị (cho admin)

**Chức năng**:
- Thêm job thủ công
- Xóa/Sửa job
- Quản lý users
- Settings

---

#### 📄 `Login.tsx`

**Nhiệm vụ**: Form đăng nhập

**Giao diện**:
```
┌──────────────────────────┐
│      🔐 Đăng nhập        │
│                          │
│  Username: [_________]   │
│  Password: [_________]   │
│                          │
│      [ Đăng nhập ]       │
└──────────────────────────┘
```

---

## 📂 PHẦN 4: DỮ LIỆU (data/)

### 📁 `data/raw/`

**Chứa**: File CSV dữ liệu thô từ crawler

**Tên file**: `topcv_jobs_YYYYMMDD_HHMMSS.csv`

**Đặc điểm**: Dữ liệu chưa xử lý, có thể có lỗi

---

### 📁 `data/processed/`

**Chứa**: File CSV dữ liệu đã xử lý

**Tên file**: `processed_topcv_jobs_YYYYMMDD_HHMMSS.csv`

**Đặc điểm**: Dữ liệu sạch, đã chuẩn hóa

---

### 📄 `data/jobs.db`

**Là gì?**: Database SQLite (file nhị phân)

**Chứa**: 
- Bảng `jobs`: 45 công việc
- Bảng `users`: Người dùng
- Bảng `admin_settings`: Cài đặt hệ thống

**Dung lượng**: ~100 KB

---

## 🔄 LUỒNG HOẠT ĐỘNG TỔNG QUÁT

### Khi khởi động lần đầu:

```
1. Chạy crawler
   python src/crawler/topcv_crawler.py
   → Tạo file data/raw/topcv_jobs_xxx.csv

2. Xử lý dữ liệu
   python src/processing/salary_parser.py
   → Tạo file data/processed/processed_topcv_jobs_xxx.csv

3. Import vào database
   python import_to_db.py
   → Tạo file data/jobs.db với 45 jobs

4. Start backend
   python -m uvicorn backend.main:app --port 8081
   → Backend chạy ở http://localhost:8081
   → Sẵn sàng nhận requests

5. Start frontend
   cd frontend && npm run dev
   → Frontend chạy ở http://localhost:5173
   → Hiển thị giao diện web
```

### Khi user sử dụng:

```
1. User mở browser: http://localhost:5173
   
2. Frontend tự động gọi API:
   GET /api/analytics/salary_distribution
   GET /api/analytics/by_location
   GET /api/analytics/by_level
   
3. Backend nhận requests:
   - Truy vấn database
   - Tính toán dữ liệu
   - Trả về JSON
   
4. Frontend nhận data:
   - Parse JSON
   - Vẽ biểu đồ
   - Hiển thị cho user

5. User click tab "Advanced Search":
   - Frontend hiển thị form
   
6. User nhập filters và click "Tìm kiếm":
   - Frontend gọi: GET /api/jobs?title=python&location=HCM&min_salary=30
   - Backend lọc dữ liệu
   - Trả về danh sách jobs matching
   - Frontend hiển thị results

7. User click "Export Excel":
   - Frontend lấy data từ state
   - Chuyển thành Excel format
   - Download file về máy
```

---

## 📊 TÓM TẮT CÁC MODULE

### 🕷️ **Module 1: Data Collection (Crawler)**
- **Files**: `topcv_crawler.py`
- **Input**: Website TopCV
- **Output**: File CSV raw
- **Nhiệm vụ**: Thu thập dữ liệu tự động

### 🧹 **Module 2: Data Processing**
- **Files**: `salary_parser.py`, `generate_diverse_data.py`
- **Input**: File CSV raw
- **Output**: File CSV processed
- **Nhiệm vụ**: Làm sạch và chuẩn hóa dữ liệu

### 💾 **Module 3: Database**
- **Files**: `models.py`, `database.py`, `import_to_db.py`
- **Input**: File CSV processed
- **Output**: File `jobs.db`
- **Nhiệm vụ**: Lưu trữ dữ liệu có cấu trúc

### ⚙️ **Module 4: Backend API**
- **Files**: `main.py`, `crud.py`, `schemas.py`, `auth.py`
- **Input**: HTTP requests từ frontend
- **Output**: JSON responses
- **Nhiệm vụ**: Xử lý logic, truy vấn database, trả về dữ liệu

### 🎨 **Module 5: Frontend UI**
- **Files**: `App.tsx`, các component trong `components/`
- **Input**: JSON từ backend
- **Output**: Giao diện web
- **Nhiệm vụ**: Hiển thị dữ liệu, tương tác với user

---

## 🎯 CÂU HỎI THƯỜNG GẶP

### Q1: Tại sao cần nhiều files như vậy?

**Trả lời**: Để code dễ quản lý và maintain.
- Mỗi file một nhiệm vụ cụ thể
- Dễ tìm bug
- Nhiều người làm cùng lúc không conflict

### Q2: Frontend và Backend giao tiếp thế nào?

**Trả lời**: Qua HTTP API
- Frontend gửi request: "Cho tôi dữ liệu X"
- Backend trả response: "Đây là dữ liệu X"
- Format: JSON (JavaScript Object Notation)

### Q3: Tại sao cần cả raw và processed data?

**Trả lời**: 
- **Raw**: Giữ nguyên để tham khảo, re-process nếu cần
- **Processed**: Dùng thực tế, đã sạch và chuẩn

### Q4: Database lưu ở đâu?

**Trả lời**: File `data/jobs.db` - là file binary
- Không cần MySQL server phức tạp
- Mở được bằng DB Browser for SQLite

### Q5: Làm sao frontend biết backend ở đâu?

**Trả lời**: Trong `App.tsx` có config:
```
const base = 'http://127.0.0.1:8081'
```

---

## 💡 LỜI KẾT

**Tóm lại dự án hoạt động như thế này**:

1. **Crawler** đi lấy dữ liệu về → Lưu vào CSV
2. **Parser** xử lý CSV → Tạo CSV sạch
3. **Import script** đọc CSV → Cho vào Database
4. **Backend** đọc Database → Tạo API
5. **Frontend** gọi API → Vẽ charts cho user

**Mỗi phần làm 1 việc riêng, nhưng kết hợp lại tạo thành hệ thống hoàn chỉnh!**

---

**File này giải thích đơn giản, không có code phức tạp.**
**Dùng để trình bày cho người không biết lập trình cũng hiểu! 😊**
