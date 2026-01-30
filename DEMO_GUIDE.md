# 📊 Job Market Crawler & Salary Analytics Platform

Một platform phân tích lương và tuyển dụng chuyên nghiệp được xây dựng bằng **FastAPI**, **React**, **TypeScript**, và **SQLite**.

## ✨ Tính Năng

### 📈 Dashboard Phân Tích
- **Biểu đồ Lương**: Phân bố salary distribution
- **Top Địa Điểm**: Mức lương trung bình theo tỉnh/thành phố
- **Theo Cấp Độ**: Mức lương theo level (Manager, Senior, etc.)

### 💼 Quản Lý Công Việc
- Xem danh sách 900+ công việc với DataGrid chuyên nghiệp
- Tìm kiếm theo chức vụ
- Sắp xếp theo lương, công ty, địa điểm
- Phân trang (10-100 jobs/trang)
- **Export XLSX** toàn bộ dữ liệu

### ⚙️ Admin Panel
- **Đăng nhập**: JWT auth (admin/demo123)
- **Thêm Job Mới**: Modal form nhập chức vụ, công ty, lương
- **Parse Lương Tự Động**: Nhập "15-25 triệu" hoặc "2000k USD" → tự chuẩn hoá
- **Trigger Crawl**: Chạy crawl job từ TopCV
- **Trigger Import**: Import CSV vào database
- **Xem Logs Real-time**: Theo dõi admin actions

### 🔐 Bảo Mật
- JWT Token authentication
- Password hashing (SHA256)
- Role-based access control (admin-only endpoints)

---

## 🚀 Cách Chạy Demo

### Cách 1: Chạy Tự Động (Windows)

**Đơn giản nhất:** Chỉ cần double-click file `run_demo.bat`

```bash
run_demo.bat
```

File này sẽ:
1. ✅ Khởi động Backend (FastAPI) trên port 8000
2. ✅ Khởi động Frontend (Vite) trên port 5173
3. ✅ Mở dashboard trong browser tự động

### Cách 2: Chạy Thủ Công (All OS)

**Bước 1: Khởi động Backend**
```bash
# Đảm bảo bạn trong thư mục project root
cd d:\job-market-crawler-salary-analytics

# Set PYTHONPATH và chạy uvicorn
set PYTHONPATH=%CD%
python -m uvicorn backend.main:app --port 8000 --host 127.0.0.1 --reload
```

**Bước 2: Khởi động Frontend (Terminal mới)**
```bash
cd d:\job-market-crawler-salary-analytics\frontend
npm run dev
```

**Bước 3: Mở Browser**
```
http://localhost:5173
```

### Cách 3: Linux/Mac
```bash
chmod +x run_demo.sh
./run_demo.sh
```

---

## 📝 Sử Dụng Dashboard

### 1️⃣ Xem Danh Sách Công Việc
- Trang chủ hiển thị 909 công việc
- **Tìm kiếm**: Nhập tên chức vụ rồi nhấn "Tìm kiếm"
- **Sắp xếp**: Click vào cột header để sort
- **Phân trang**: Chọn số job/trang ở dưới
- **Export**: Nhấn "Xuất XLSX" để download

### 2️⃣ Đăng Nhập Admin
- Cuộn xuống, nhấn **"Đăng Nhập Admin"**
- Nhập: `admin` / `demo123`
- ✅ Login thành công → Hiện **Bảng Điều Khiển Admin**

### 3️⃣ Thêm Job Mới
- Nhấn **"+ Thêm Job"** trong Admin Panel
- Điền:
  - **Chức vụ**: VD "Senior Developer"
  - **Công ty**: VD "FPT Software"
  - **Cấp độ**: VD "Senior" (optional)
  - **Địa điểm**: VD "Hà Nội" (optional)
  - **Lương**: VD "20 - 30 triệu" hoặc "2000 USD/tháng"
- Nhấn **"Parse"** → Tự động chuẩn hoá thành triệu VND
- Nhấn **"Lưu"** → Job được thêm vào database

### 4️⃣ Quản Lý Crawl
- **Bật/Tắt Crawl**: Toggle trạng thái crawl tự động
- **Nhập Dữ liệu**: Trigger import từ CSV files
- **Chạy Crawl**: Trigger crawl jobs từ TopCV
- **Xem Logs**: Theo dõi hoạt động admin

---

## 📊 Endpoints API

### Public (Không cần auth)
```
GET  /api/health                          # Health check
GET  /api/jobs?page=1&per_page=50        # Danh sách jobs (sort, filter, pagination)
GET  /api/jobs/{id}                      # Chi tiết 1 job
GET  /api/analytics/salary_distribution   # Distribution of salaries
GET  /api/analytics/by_location           # Avg salary by location
GET  /api/analytics/by_level              # Avg salary by level
GET  /api/metadata                        # Locations, levels for filters
POST /api/parse_salary                    # Parse salary string → normalized VND
POST /api/auth/login                      # Login (username/password)
```

### Admin Only (Cần JWT token)
```
POST /api/admin/jobs/create               # Thêm job mới
POST /api/admin/import                    # Trigger import CSV
POST /api/admin/crawl                     # Trigger crawl TopCV
POST /api/admin/toggle_crawl              # Bật/tắt crawl
GET  /api/admin/logs?lines=100            # Xem logs
GET  /api/admin/settings                  # Xem settings
```

---

## 🏗️ Cấu Trúc Project

```
job-market-crawler-salary-analytics/
├── backend/                    # FastAPI backend
│   ├── main.py                # Routes & endpoints
│   ├── models.py              # SQLAlchemy models (Job, User, AdminSetting)
│   ├── crud.py                # Database queries
│   ├── database.py            # SQLite engine
│   ├── auth.py                # JWT + password hashing
│   ├── schemas.py             # Pydantic schemas
│   └── import_data.py         # CSV import script
├── frontend/                  # React + Vite + TypeScript
│   ├── src/
│   │   ├── App.tsx            # Main component
│   │   ├── components/
│   │   │   ├── JobList.tsx    # DataGrid with jobs
│   │   │   ├── Login.tsx      # Login form
│   │   │   ├── AdminPanel.tsx # Admin controls
│   │   │   └── AddJobModal.tsx # Add job modal
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── src/                       # Legacy scripts
│   ├── crawler/topcv_crawler.py      # TopCV crawler
│   ├── processing/salary_parser.py   # Salary normalization
│   └── analytics/basic_analyzer.py   # Analytics
├── data/
│   ├── jobs.db               # SQLite database (909 jobs)
│   ├── raw/                  # Raw CSV files
│   └── processed/            # Processed CSV files
├── run_demo.bat              # Windows launcher
├── run_demo.sh               # Linux/Mac launcher
└── README.md                 # This file
```

---

## 🔧 Yêu Cầu Hệ Thống

### Backend
- Python 3.11+
- FastAPI, SQLAlchemy, pandas, python-jose
- SQLite (included)

### Frontend
- Node.js 16+
- npm, React 18, TypeScript, Material-UI, Vite

### Database
- SQLite3 (file: `data/jobs.db`)
- 909 pre-imported jobs

---

## 🎯 Tính Năng Nâng Cao (Có sẵn)

✅ **Salary Parsing**: "15 - 25 triệu", "từ 10 triệu", "2000k USD" → chuẩn hoá  
✅ **Server-side Pagination**: Xử lý 900+ records hiệu quả  
✅ **Real-time Logs**: Theo dõi admin actions  
✅ **XLSX Export**: Download toàn bộ jobs với headers  
✅ **Responsive Design**: Desktop, tablet, mobile  
✅ **Error Handling**: API errors hiển thị user-friendly  

---

## 📝 Default Credentials

```
Username: admin
Password: demo123
```

---

## 🐛 Troubleshooting

### Port 8000 hoặc 5173 bị chiếm
```bash
# Windows: Kill process sử dụng port
netstat -ano | findstr :8000
taskkill /pid <PID> /f

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Module not found errors
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### Database lỗi
```bash
# Reset database
rm data/jobs.db
python do_import.py
```

---

## 📧 Support

Nếu gặp vấn đề, kiểm tra:
1. Backend logs (terminal chạy uvicorn)
2. Frontend console (F12 → Console tab)
3. Network tab để xem API calls

---

**Developed with ❤️ using FastAPI + React + TypeScript**

Happy analyzing! 📊
