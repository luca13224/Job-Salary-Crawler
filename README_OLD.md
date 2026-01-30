# Topic: Job Market Crawler & Salary Analytics

Dự án này tập trung vào việc xây dựng một hệ thống thu thập và phân tích dữ liệu tuyển dụng ngành IT tại Việt Nam, với mục tiêu chính là phân tích mức lương theo các tiêu chí khác nhau.

##  tính năng chính

- **Crawler**: Thu thập dữ liệu việc làm (chức danh, công ty, lương, địa điểm) từ trang web TopCV.vn.
- **Data Processor**: Làm sạch và chuẩn hóa dữ liệu thô. Đặc biệt, chuẩn hóa các định dạng lương đa dạng về một đơn vị duy nhất (triệu VND).
- **Analyzer**: Thực hiện các phân tích thống kê cơ bản trên dữ liệu đã xử lý để tìm ra xu hướng về lương theo địa điểm và cấp bậc.
- **Jupyter Notebook**: Trình bày quá trình phân tích một cách trực quan, phù hợp cho việc báo cáo và demo.
- **Web Demo**: Một trang web đơn giản xây dựng bằng Flask để trình bày kết quả phân tích.

## Phân công thành viên

| STT | Họ và tên          | MSSV       | Vai trò         | Nhiệm vụ chính                                      |
|:----|:------------------ |:-----------|:----------------|:----------------------------------------------------|
| 1   | Trần Văn Chiến     | 2251161958 |  Trưởng nhóm    | Phụ trách tổng thể, tích hợp module, báo cáo        |
| 2   |Nguyễn Ngọc Tuấn Anh| 2251161940 | Thành viên      | Xây dựng module thu thập dữ liệu (Crawler)          |
| 3   | Hoàng Anh Khoa     | 2251162045 | Thành viên      | Xây dựng module xử lý và chuẩn hóa dữ liệu          |
| 4   | Hà Tiến Lực        | 2251162067 | Thành viên      | Xây dựng module phân tích và trực quan hóa dữ liệu  |
| 5   | Nguyễn Hữu Minh    | 2251162073 | Thành viên      | Thiết kế và triển khai Web Demo (Flask)             |

## Mô tả các thành phần mã nguồn

Dưới đây là mô tả chi tiết về chức năng của các file mã nguồn chính trong dự án:

-   **`src/crawler/topcv_crawler.py`**: Chịu trách nhiệm thu thập dữ liệu tuyển dụng từ trang TopCV. Module này truy cập vào các trang danh sách việc làm, trích xuất thông tin chi tiết như chức danh, công ty, mức lương, địa điểm và lưu trữ dưới dạng file CSV thô.
-   **`src/processing/salary_parser.py`**: Thực hiện việc làm sạch và chuẩn hóa dữ liệu từ file CSV thô. Nhiệm vụ cốt lõi là phân tích và chuyển đổi các chuỗi mô tả lương (ví dụ: "15-20 triệu", "Thương lượng", "Up to $1000") về một định dạng số thống nhất (đơn vị: triệu VND) để phục vụ cho việc phân tích.
-   **`src/analytics/basic_analyzer.py`**: Đọc dữ liệu đã được xử lý để thực hiện các phân tích thống kê. Cụ thể, file này tính toán mức lương trung bình theo cấp bậc và theo địa điểm, sau đó lưu kết quả phân tích (biểu đồ) vào thư mục `web/static`.
-   **`notebooks/llm_analysis.ipynb`**: Là một Jupyter Notebook dùng để trình bày và minh họa quá trình phân tích dữ liệu một cách chi tiết, từ bước đọc dữ liệu, xử lý, cho đến việc tạo ra các biểu đồ và nhận xét kết quả.
-   **`web/app.py`**: File chính của ứng dụng web Flask. Nó có nhiệm vụ khởi tạo server, định tuyến các trang (trang chủ, trang phân tích) và hiển thị các kết quả phân tích (biểu đồ) đã được tạo ra từ `basic_analyzer.py` lên giao diện HTML.

## Cấu trúc thư mục

```
job-salary-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── llm_analysis.ipynb
│
├── results/
│   └── charts/
│
├── src/
│   ├── crawler/
│   ├── processing/
│   └── analytics/
│
├── web/
│   ├── static/         # Chứa file tĩnh (biểu đồ đã tạo)
│   ├── templates/      # Chứa các file HTML
│   └── app.py          # File chạy web app Flask
│
├── requirements.txt
└── README.md
```

## Hướng dẫn chạy hệ thống (Dòng lệnh)

### Bước 1: Cài đặt môi trường

1.  **Tạo môi trường ảo** (khuyến khích):
    ```bash
    python -m venv venv
    ```
    Kích hoạt môi trường ảo: `venv\Scripts\activate` (Windows) hoặc `source venv/bin/activate` (macOS/Linux).

2.  **Cài đặt các thư viện cần thiết**:
    ```bash
    pip install -r requirements.txt
    ```

### Bước 2: Thu thập dữ liệu
```bash
python -m src.crawler.topcv_crawler
```

### Bước 3: Xử lý dữ liệu
```bash
python -m src.processing.salary_parser
```

### Bước 4: Chạy phân tích
```bash
python -m src.analytics.basic_analyzer
```

### Bước 5: Xem Notebook phân tích
```bash
jupyter notebook
```

---

### Chạy demo toàn bộ (tạo dữ liệu mẫu -> xử lý -> phân tích -> (tùy chọn) khởi động web)
Bạn có thể dùng script `run_demo.py` để chạy toàn bộ pipeline một cách nhanh chóng:

```bash
# Chạy pipeline (sẽ tạo data/raw/topcv_demo_raw.csv -> data/processed/processed_topcv_demo_raw.csv -> results charts)
python run_demo.py

# Chạy pipeline và khởi động web demo (mở trình duyệt):
python run_demo.py --serve
```

---

## Chạy phiên bản chuyên nghiệp (Option B) — không dùng Docker
Hướng dẫn nhanh để chạy backend FastAPI (SQLite) và frontend React (Vite) trên máy local.

### Backend
1. Cài dependencies cho backend

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

2. Import dữ liệu đã xử lý vào SQLite DB

```powershell
python -c "from backend import import_data; import_data.import_processed_csvs()"
```

3. Chạy backend (uvicorn)

```powershell
uvicorn backend.main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

### Frontend
1. Cài dependencies cho frontend (cần Node.js >= 18)

```bash
cd frontend
npm install
npm run dev
```

2. Mở trình duyệt vào http://127.0.0.1:5173 — frontend sẽ gọi API backend trên `http://127.0.0.1:8000`.

#### Tính năng UI (Job Listings)
- **Bộ lọc**: tìm theo Title, Location, Level, khoảng lương (Min/Max). Metadata location/level được lấy từ backend (`GET /api/metadata`).
- **Sắp xếp**: chọn sắp xếp theo Lương trung bình / Title / Company (asc/desc).
- **Modal chi tiết**: click vào một hàng để xem thông tin chi tiết và link tới tin tuyển dụng.
- **Export**: có hai tùy chọn: export toàn bộ (server) via `GET /api/jobs/export`, hoặc export page hiện tại (client-side CSV) or export XLSX (DataGrid button).

#### Auth & Admin
- Default admin user (username: `admin`, password: `demo123`) được tạo khi import dữ liệu.
- Đăng nhập từ UI (Admin login box). Sau khi đăng nhập, bạn có thể truy cập **Admin Panel** để bật/tắt crawl, trigger import, trigger crawl và xem logs.
- Endpoints quan trọng:
  - `POST /api/auth/login` (OAuth2 password)
  - `POST /api/admin/import`, `POST /api/admin/crawl`, `POST /api/admin/toggle_crawl`, `GET /api/admin/logs`, `GET /api/admin/settings`



---

## Hướng dẫn chạy Web Demo

Web demo sử dụng dữ liệu mẫu được tạo sẵn (`data/processed/processed_demo_data.csv`).

### Bước 1: Cài đặt môi trường
Đảm bảo bạn đã cài đặt tất cả các thư viện từ `requirements.txt`.

### Bước 2: Chạy Web App

1.  **Thiết lập biến môi trường cho Flask.**
    -   Trên Windows (PowerShell):
        ```powershell
        $env:FLASK_APP = "web/app.py"
        ```
    -   Trên macOS/Linux:
        ```bash
        export FLASK_APP=web/app.py
        ```

2.  **Khởi động server Flask:**
    ```bash
    flask run
    ```

3.  Mở trình duyệt và truy cập vào địa chỉ `http://127.0.0.1:5000` để xem kết quả.
