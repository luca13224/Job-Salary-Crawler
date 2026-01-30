# 🚀 Hướng Dẫn Sử Dụng Dữ Liệu Thật từ TopCV

## ✨ Đã Hoàn Thành

Hệ thống đã được cấu hình để sử dụng **dữ liệu thật từ TopCV** thay vì fake data.

### 📊 Dataset Hiện Tại
- **Tên**: "TopCV IT Jobs - Real Data (2026-01-30)"
- **Số lượng**: 36 jobs thật được crawler từ TopCV
- **Nguồn**: https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026

## 🔄 Cách Cập Nhật Dữ Liệu Mới

### Option 1: Chạy Pipeline Tự Động (Khuyến nghị)

**Windows PowerShell:**
```powershell
.\run_full_pipeline.ps1
```

Pipeline này sẽ tự động:
1. 📡 Crawl job listings từ TopCV (10 pages)
2. ⚙️ Process salary data
3. 💾 Import vào database

### Option 2: Chạy Từng Bước Thủ Công

```powershell
# Step 1: Crawl dữ liệu từ TopCV
python src/crawler/topcv_crawler.py

# Step 2: Process salary data
python src/processing/salary_parser.py

# Step 3: Import vào database
python import_to_db.py
```

## 📁 Cấu Trúc Dữ Liệu

```
data/
├── raw/                    # Dữ liệu thô từ crawler
│   └── topcv_jobs_*.csv   # Files crawled từ TopCV
├── processed/              # Dữ liệu đã xử lý
│   └── processed_*.csv    # Files đã parse salary
└── jobs.db                 # SQLite database (dữ liệu thật)
```

## 🎯 Các Thành Phần

### 1. Crawler (`src/crawler/topcv_crawler.py`)
- Crawl job listings từ TopCV
- Lưu vào `data/raw/topcv_jobs_*.csv`
- Mặc định: 10 pages (~100-200 jobs)

### 2. Salary Parser (`src/processing/salary_parser.py`)
- Parse salary strings (VND, USD)
- Chuyển đổi sang triệu VND
- Tính average salary
- Output: `data/processed/processed_*.csv`

### 3. Database Importer (`import_to_db.py`)
- Xóa dữ liệu cũ
- Import dữ liệu mới vào SQLite
- Đặt tên dataset với timestamp

## 🌐 Xem Kết Quả

1. **Khởi động backend** (nếu chưa chạy):
   ```powershell
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081 --reload
   ```

2. **Truy cập web app**:
   - Frontend: http://localhost:5174
   - API: http://localhost:8081/api/jobs

3. **Refresh browser** để thấy dữ liệu thật từ TopCV

## 📊 API Endpoints với Dữ Liệu Thật

```bash
# Xem tất cả jobs
GET http://localhost:8081/api/jobs

# Analytics - Salary by location
GET http://localhost:8081/api/analytics/by_location

# Analytics - Salary by level
GET http://localhost:8081/api/analytics/by_level

# Analytics - Salary distribution
GET http://localhost:8081/api/analytics/salary_distribution
```

## ⚙️ Tùy Chỉnh

### Crawl nhiều pages hơn
Edit `src/crawler/topcv_crawler.py`:
```python
num_pages = 20  # Thay đổi từ 10 sang 20
```

### Crawl từ nguồn khác
- Thêm crawler mới trong `src/crawler/`
- Follow pattern của `topcv_crawler.py`
- Dataset name sẽ tự động cập nhật

## 🔍 Kiểm Tra Dữ Liệu

```powershell
# Xem số lượng jobs trong database
python -c "from backend.database import SessionLocal; from backend.models import Job; print(f'Total jobs: {SessionLocal().query(Job).count()}')"

# Xem file crawled mới nhất
Get-ChildItem data/raw/*.csv | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Xem file processed mới nhất
Get-ChildItem data/processed/*.csv | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

## 💡 Tips

1. **Crawl định kỳ**: Chạy pipeline hàng ngày để cập nhật data mới
2. **Backup data**: File CSV trong `data/raw/` là backup của dữ liệu đã crawl
3. **Dataset naming**: Mỗi lần import sẽ tự động đặt tên với timestamp
4. **Error handling**: Crawler sẽ bỏ qua jobs lỗi và tiếp tục crawl

## 🚨 Troubleshooting

### Crawler không lấy được data
- Kiểm tra internet connection
- Website có thể đã thay đổi cấu trúc HTML
- Xem log trong console để debug

### Import lỗi
- Đảm bảo file processed tồn tại trong `data/processed/`
- Check format của CSV file
- Xem error message trong console

### Backend không hiển thị data
- Restart backend server
- Clear browser cache (Ctrl+F5)
- Check API endpoint trả về data: http://localhost:8081/api/jobs

## 📝 Ghi Chú

- **Fake data đã bị xóa**: Database hiện chỉ chứa dữ liệu thật từ TopCV
- **Source tracking**: Mỗi job có field `source` để biết nguồn data
- **Timestamp**: Field `crawled_at` ghi lại thời gian crawl
