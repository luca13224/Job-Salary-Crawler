# 📊 Job Market Crawler & Salary Analytics Platform

**Nền tảng phân tích thị trường lao động và mức lương cho ngành IT tại Việt Nam**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)

## 🎯 Tổng Quan

Platform phân tích dữ liệu việc làm và mức lương trong ngành công nghệ Việt Nam, cung cấp:
- 📈 Biểu đồ phân tích mức lương theo cấp độ, địa điểm
- 🏢 Top công ty tuyển dụng
- 💼 Phân tích kỹ năng (skills) được yêu cầu nhiều nhất
- 🔍 Tìm kiếm và lọc công việc nâng cao
- 📊 Dashboard analytics tổng quan

## 🚀 Tính Năng

### 📱 Frontend (React + TypeScript + Material-UI)
- **Dashboard Cơ Bản**: Biểu đồ salary distribution, top locations, job levels
- **Phân Tích Nâng Cao**: Statistics nâng cao, top skills, company analysis
- **Tìm Kiếm Nâng Cao**: Filter theo title, company, location, level, salary range
- **Top 30 Cao Lương**: Danh sách các vị trí lương cao nhất
- **Nguồn Dữ Liệu**: Market overview và trending jobs
- **Danh Sách Công Việc**: Bảng jobs với search và export XLSX

### ⚙️ Backend (FastAPI + SQLite)
- RESTful API với FastAPI
- SQLite database cho data persistence
- 15+ analytics endpoints
- CORS enabled cho frontend development
- Auto-reload trong development mode

### 🕷️ Data Collection & Processing
- Web crawler cho TopCV và các job boards
- Salary parser hỗ trợ nhiều format (VND, USD, ranges)
- Data processing pipeline tự động
- Generate diverse realistic dataset cho testing

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.11 hoặc cao hơn
- **Node.js**: 18.x hoặc cao hơn
- **npm** hoặc **yarn**: Package manager
- **Git**: Để clone repository

## 🛠️ Cài Đặt

### 1️⃣ Clone Repository

```bash
git clone https://github.com/luca13224/Job-Salary-Crawler.git
cd Job-Salary-Crawler
```

### 2️⃣ Setup Backend

#### Windows:
```powershell
# Tạo virtual environment
python -m venv env

# Activate virtual environment
.\env\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
# Tạo virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 3️⃣ Setup Frontend

```bash
cd frontend
npm install
# hoặc
yarn install
```

### 4️⃣ Tạo Database và Import Data

```bash
# Quay về root directory
cd ..

# Generate diverse dataset (45 jobs realistic)
python generate_diverse_data.py

# Process salary data
python src/processing/salary_parser.py

# Import vào database
python import_to_db.py
# (Nhập "yes" khi được hỏi confirm)
```

**Hoặc crawl data thật từ TopCV:**
```bash
python src/crawler/topcv_crawler.py
python src/processing/salary_parser.py
python import_to_db.py
```

## 🎮 Chạy Ứng Dụng

### Cách 1: Chạy Development Mode (Khuyến nghị)

**Mở 2 terminals:**

**Terminal 1 - Backend:**
```bash
# Từ root directory, activate virtual environment nếu chưa
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# hoặc
yarn dev
```

**Truy cập:**
- **Frontend**: http://localhost:5173 (hoặc 5174)
- **Backend API**: http://localhost:8081
- **API Docs (Swagger)**: http://localhost:8081/docs

### Cách 2: Script Tự Động (Windows)

```powershell
# Start backend trong background window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081 --reload"

# Đợi backend khởi động
Start-Sleep -Seconds 5

# Start frontend
cd frontend
npm run dev
```

## 📊 Dataset

**Dataset mặc định**: 45 jobs từ các công ty công nghệ hàng đầu VN

### 📈 Thống kê:
- **Companies**: 40+ công ty (VNG, Tiki, FPT Software, Shopee, Grab, Samsung, Zalo, VNPAY, etc.)
- **Locations**: 
  - Hồ Chí Minh: 20 jobs (avg 46 triệu)
  - Hà Nội: 20 jobs (avg 42 triệu)
  - Đà Nẵng: 3 jobs (avg 28.8 triệu)
  - Remote: 2 jobs (avg 42.5 triệu)
- **Levels**: 
  - Manager: 4 jobs (110 triệu avg)
  - Lead: 3 jobs (72.5 triệu avg)
  - Senior: 10 jobs (55 triệu avg)
  - Mid-level: 17 jobs (34.7 triệu avg)
  - Junior: 11 jobs (12.4 triệu avg)
- **Salary Range**: 7-200 triệu VND/tháng
- **Top Skills**: React (7), Java (7), JavaScript (6), Python (6), Node.js (5), AWS (4)

### 🔄 Cập nhật data mới:

```bash
# Option 1: Generate diverse dataset
python generate_diverse_data.py
python src/processing/salary_parser.py
python import_to_db.py

# Option 2: Crawl từ TopCV (cần internet)
python src/crawler/topcv_crawler.py
python src/processing/salary_parser.py
python import_to_db.py
```

## 🗂️ Cấu Trúc Project

```
job-market-crawler-salary-analytics/
├── backend/                       # FastAPI backend
│   ├── main.py                   # API routes & endpoints
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic schemas
│   ├── database.py               # Database configuration
│   ├── crud.py                   # Database CRUD operations
│   └── auth.py                   # Authentication (if needed)
│
├── frontend/                      # React + TypeScript frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── AdvancedAnalytics.tsx
│   │   │   ├── AdvancedSearch.tsx
│   │   │   ├── DataSources.tsx
│   │   │   ├── JobList.tsx
│   │   │   └── Top30Jobs.tsx
│   │   ├── App.tsx               # Main app component
│   │   └── main.tsx              # Entry point
│   ├── package.json              # NPM dependencies
│   └── vite.config.ts            # Vite configuration
│
├── src/
│   ├── crawler/                  # Web crawlers
│   │   └── topcv_crawler.py     # TopCV crawler implementation
│   ├── processing/               # Data processing
│   │   └── salary_parser.py     # Parse & normalize salary
│   └── analytics/                # Analytics modules
│       └── basic_analyzer.py
│
├── data/
│   ├── raw/                      # Raw crawler data (CSV)
│   ├── processed/                # Processed data (CSV)
│   └── jobs.db                   # SQLite database (gitignored)
│
├── generate_diverse_data.py      # Generate demo dataset
├── import_to_db.py               # Import CSV → SQLite
├── add_salary_estimates.py       # Add salary estimates to NULL
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Documentation (this file)
```

## 🔌 API Endpoints

### 📋 Jobs Endpoints
- `GET /api/jobs` - Danh sách jobs với pagination & filters
  - Query params: `title`, `location`, `level`, `min_salary`, `max_salary`, `page`, `per_page`
- `GET /api/jobs/{id}` - Chi tiết 1 job
- `GET /api/metadata` - Metadata (available filters)
- `GET /api/health` - Health check

### 📊 Analytics Endpoints
- `GET /api/analytics/salary-stats` - Thống kê lương tổng quan
- `GET /api/analytics/salary-by-level` - Lương theo cấp độ
- `GET /api/analytics/salary-by-location` - Lương theo địa điểm
- `GET /api/analytics/by_location` - Alias cho salary-by-location
- `GET /api/analytics/by_level` - Alias cho salary-by-level
- `GET /api/analytics/salary_distribution` - Phân bố lương
- `GET /api/analytics/top-skills?limit=15` - Top kỹ năng
- `GET /api/analytics/company-analysis?limit=12` - Top công ty
- `GET /api/analytics/title-salary-insights?limit=10` - Insights theo title
- `GET /api/analytics/market-overview` - Market overview
- `GET /api/analytics/data-sources` - Data sources info
- `GET /api/analytics/trending-jobs` - Trending jobs
- `GET /api/analytics/top-30-jobs` - Top 30 jobs cao lương

**Chi tiết đầy đủ**: http://localhost:8081/docs (Swagger UI)

## 🎨 Screenshots

### Dashboard Cơ Bản
- Phân bố lương (histogram)
- Top địa điểm cao lương
- Phân bố theo cấp độ

### Phân Tích Nâng Cao
- Salary statistics cards
- Top skills analysis
- Company analysis
- Title-salary insights

### Tìm Kiếm Nâng Cao
- Multi-criteria filters
- Real-time search
- Data table với sorting

## 📝 Development Notes

### Tech Stack:
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Frontend**: React 18, TypeScript, Material-UI, Recharts, Chart.js
- **Database**: SQLite (development), có thể scale lên PostgreSQL
- **Build Tool**: Vite (frontend), pip (backend)

### Code Quality:
- TypeScript strict mode enabled
- Python type hints
- ESLint configured
- Responsive design with Material-UI

## 🐛 Troubleshooting

### Backend không khởi động:
```bash
# Kiểm tra Python version
python --version  # Cần >= 3.11

# Kiểm tra virtual environment đã activate chưa
# Windows: .\env\Scripts\activate
# Linux/Mac: source env/bin/activate

# Cài lại dependencies
pip install -r requirements.txt

# Kiểm tra port 8081 có bị chiếm không
netstat -ano | findstr :8081  # Windows
lsof -i :8081  # Linux/Mac
```

### Frontend không chạy:
```bash
# Kiểm tra Node version
node --version  # Cần >= 18

# Xóa cache và reinstall
rm -rf node_modules package-lock.json
npm install

# Thử port khác
npm run dev -- --port 5174
```

### Database trống:
```bash
# Generate lại data
python generate_diverse_data.py
python src/processing/salary_parser.py
python import_to_db.py

# Kiểm tra file database
ls -la data/jobs.db  # Linux/Mac
dir data\jobs.db     # Windows
```

### CORS errors:
- Đảm bảo backend chạy trên port 8081
- Kiểm tra frontend config trong `App.tsx`: `base = 'http://127.0.0.1:8081'`
- Backend đã enable CORS cho all origins trong development

### Charts không hiển thị:
- Refresh browser (Ctrl+F5 để clear cache)
- Kiểm tra browser console có error không (F12)
- Verify API endpoints trả về data: http://localhost:8081/api/analytics/by_level

## 👥 Team Members

| STT | Họ và tên          | MSSV       | Vai trò         | Nhiệm vụ chính                                      |
|:----|:------------------ |:-----------|:----------------|:----------------------------------------------------|
| 1   | Trần Văn Chiến     | 2251161958 | Trưởng nhóm     | Tổng thể, tích hợp, báo cáo                        |
| 2   | Nguyễn Ngọc Tuấn Anh| 2251161940 | Thành viên     | Module thu thập dữ liệu (Crawler)                  |
| 3   | Hoàng Anh Khoa     | 2251162045 | Thành viên      | Module xử lý và chuẩn hóa dữ liệu                  |
| 4   | Hà Tiến Lực        | 2251162067 | Thành viên      | Module phân tích và trực quan hóa                   |

## 🤝 Contributing

Mọi đóng góp đều được chào đón! Để contribute:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📧 Contact

- **GitHub**: [@luca13224](https://github.com/luca13224)
- **Repository**: [Job-Salary-Crawler](https://github.com/luca13224/Job-Salary-Crawler)

## 📜 License

Dự án này được phát hành dưới MIT License.

---

⭐ **Star repository này nếu bạn thấy hữu ích!**

**Made with ❤️ for Vietnam Tech Community**
