# 🏗️ KIẾN TRÚC VÀ LUỒNG HOẠT ĐỘNG DỰ ÁN

## 📋 Tổng Quan Hệ Thống

Dự án **Job Market Crawler & Salary Analytics** là một hệ thống web full-stack gồm 3 tầng chính:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)            │
│         - Giao diện người dùng với Material-UI              │
│         - Biểu đồ phân tích (Chart.js, Recharts)           │
│         - Tìm kiếm và lọc dữ liệu nâng cao                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│         - RESTful API endpoints                             │
│         - Business logic & Analytics                        │
│         - Authentication & Authorization                    │
└────────────────────┬────────────────────────────────────────┘
                     │ SQLAlchemy ORM
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                        │
│         - Lưu trữ thông tin công việc                      │
│         - User management                                   │
│         - System settings                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 LUỒNG HOẠT ĐỘNG CHÍNH

### **1️⃣ Giai Đoạn Thu Thập Dữ Liệu (Data Collection)**

#### **Module: Web Crawler** (`src/crawler/topcv_crawler.py`)

```python
# Luồng hoạt động của crawler:

1. Khởi tạo requests với User-Agent giả lập browser
2. Gửi HTTP GET request đến TopCV search page
3. Parse HTML bằng BeautifulSoup4
4. Trích xuất thông tin:
   - Tiêu đề công việc (Job Title)
   - Tên công ty (Company Name)
   - Địa điểm (Location)
   - Mức lương (Salary - raw text)
   - Cấp độ (Level: Junior/Mid/Senior/Lead/Manager)
   - URL chi tiết
5. Lưu vào CSV file (raw data)
```

**Code chính:**
```python
def crawl_jobs(num_pages=1):
    all_jobs = []
    for page in range(1, num_pages + 1):
        url = f"{BASE_URL}?page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse từng job listing
        for job_card in soup.find_all('div', class_='job-item'):
            job_data = {
                'title': extract_title(job_card),
                'company': extract_company(job_card),
                'salary': extract_salary(job_card),
                'location': extract_location(job_card),
                'level': extract_level(job_card),
                'url': extract_url(job_card)
            }
            all_jobs.append(job_data)
    
    return pd.DataFrame(all_jobs)
```

**Output:** `data/raw/topcv_jobs_YYYYMMDD_HHMMSS.csv`

---

### **2️⃣ Giai Đoạn Xử Lý Dữ Liệu (Data Processing)**

#### **Module: Salary Parser** (`src/processing/salary_parser.py`)

```python
# Luồng xử lý salary:

1. Đọc raw CSV file
2. Parse salary string phức tạp:
   - "15-20 triệu" → min=15, max=20
   - "Lên đến 30 triệu" → max=30
   - "Từ 2000 USD" → convert to VND
   - "Thỏa thuận" → NULL (negotiable)
3. Chuẩn hóa đơn vị về "triệu VND"
4. Tính mức lương trung bình (avg_salary_mil_vnd)
5. Làm sạch dữ liệu:
   - Remove duplicates
   - Handle NULL values
   - Standardize location/level names
6. Save processed data
```

**Logic Parse Salary:**
```python
def parse_salary(salary_str):
    # 1. Detect currency (VND/USD)
    currency = 'VND'
    if 'usd' in salary_str.lower() or '$' in salary_str:
        currency = 'USD'
    
    # 2. Extract numbers with regex
    # Pattern: "15-20 triệu" or "Từ 2000 USD"
    match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', salary_str)
    if match:
        min_val = float(match.group(1))
        max_val = float(match.group(2))
        
    # 3. Convert USD to VND if needed
    if currency == 'USD':
        min_val *= USD_TO_VND_RATE / 1_000_000  # Convert to triệu VND
        max_val *= USD_TO_VND_RATE / 1_000_000
    
    # 4. Calculate average
    avg_salary = (min_val + max_val) / 2
    
    return min_val, max_val, avg_salary, currency
```

**Output:** `data/processed/processed_topcv_jobs_YYYYMMDD_HHMMSS.csv`

---

### **3️⃣ Giai Đoạn Import Vào Database**

#### **Script: import_to_db.py**

```python
# Luồng import:

1. Kết nối SQLite database (data/jobs.db)
2. Clear old data (optional)
3. Đọc processed CSV
4. Map CSV columns → Database columns
5. Bulk insert vào table 'jobs'
6. Commit transaction
7. Verify import thành công
```

**Database Schema (models.py):**
```python
class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True)           # "Senior Backend Developer"
    company = Column(String(256), index=True)         # "VNG Corporation"
    level = Column(String(64), index=True)            # "Senior"
    salary_raw = Column(String(128))                  # "15-20 triệu"
    avg_salary_mil_vnd = Column(Float, index=True)    # 17.5
    location = Column(String(256), index=True)        # "Ho Chi Minh"
    skills = Column(Text)                             # "Python, FastAPI, PostgreSQL"
    source = Column(String(128))                      # "TopCV"
    url = Column(String(512))                         # "https://..."
    crawled_at = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### **4️⃣ Giai Đoạn Backend API**

#### **Module: FastAPI Backend** (`backend/main.py`)

**Kiến trúc 3 tầng:**
```
Controller (main.py) → Service (crud.py) → Model (models.py)
        ↓                      ↓                   ↓
   HTTP Routes          Business Logic         Database ORM
```

#### **A. Jobs Endpoints**

**GET /api/jobs** - Danh sách công việc với filters & pagination
```python
@app.get('/api/jobs')
def get_jobs(
    title: str = None,           # Filter theo title
    location: str = None,         # Filter theo location
    level: str = None,            # Filter theo level
    min_salary: float = None,     # Lương tối thiểu
    max_salary: float = None,     # Lương tối đa
    sort_by: str = None,          # Sắp xếp theo field
    page: int = 1,                # Pagination
    per_page: int = 50,
    db: Session = Depends(get_db)
):
    # 1. Build query với filters
    q = db.query(models.Job)
    if title:
        q = q.filter(models.Job.title.ilike(f"%{title}%"))
    if location:
        q = q.filter(models.Job.location.ilike(f"%{location}%"))
    # ... more filters
    
    # 2. Apply sorting
    if sort_by == 'avg_salary':
        q = q.order_by(models.Job.avg_salary_mil_vnd.desc())
    
    # 3. Pagination
    skip = (page - 1) * per_page
    results = q.offset(skip).limit(per_page).all()
    total = q.count()
    
    return {'total': total, 'page': page, 'items': results}
```

**GET /api/jobs/{id}** - Chi tiết 1 công việc
```python
@app.get('/api/jobs/{job_id}')
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    return job
```

#### **B. Analytics Endpoints**

**1. Salary Distribution** - Phân bố mức lương
```python
@app.get('/api/analytics/salary_distribution')
def salary_distribution(db: Session = Depends(get_db)):
    # Lấy tất cả mức lương để vẽ histogram
    salaries = db.query(models.Job.avg_salary_mil_vnd)\
                 .filter(models.Job.avg_salary_mil_vnd != None)\
                 .all()
    
    values = [s[0] for s in salaries]
    return {'values': sorted(values)}
```

**2. Average Salary by Location**
```python
@app.get('/api/analytics/by_location')
def avg_by_location(db: Session = Depends(get_db)):
    results = db.query(
        models.Job.location,
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary'),
        func.count(models.Job.id).label('job_count')
    ).filter(
        models.Job.avg_salary_mil_vnd.isnot(None)
    ).group_by(
        models.Job.location
    ).order_by(
        func.avg(models.Job.avg_salary_mil_vnd).desc()
    ).limit(10).all()
    
    return {
        'data': [
            {
                'location': r[0],
                'avg_salary': round(r[1], 2),
                'job_count': r[2]
            } for r in results
        ]
    }
```

**3. Average Salary by Level**
```python
@app.get('/api/analytics/by_level')
def avg_by_level(db: Session = Depends(get_db)):
    # Tương tự by_location nhưng group by level
    # Trả về: Junior, Mid-level, Senior, Lead, Manager
    # với avg_salary và job_count tương ứng
```

**4. Top Skills**
```python
@app.get('/api/analytics/top-skills')
def top_skills(limit: int = 15, db: Session = Depends(get_db)):
    # Parse skills column (comma-separated)
    # Count frequency của từng skill
    # Return top N skills most required
    
    all_skills = []
    jobs = db.query(models.Job.skills).filter(models.Job.skills != None).all()
    
    for job in jobs:
        skills_list = job[0].split(',')
        all_skills.extend([s.strip() for s in skills_list])
    
    # Count frequency
    from collections import Counter
    skill_counts = Counter(all_skills)
    
    return {
        'data': [
            {'skill': skill, 'count': count}
            for skill, count in skill_counts.most_common(limit)
        ]
    }
```

**5. Company Analysis**
```python
@app.get('/api/analytics/company-analysis')
def company_analysis(limit: int = 12, db: Session = Depends(get_db)):
    # Top companies by number of jobs posted
    results = db.query(
        models.Job.company,
        func.count(models.Job.id).label('job_count'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary')
    ).filter(
        models.Job.company.isnot(None)
    ).group_by(
        models.Job.company
    ).order_by(
        func.count(models.Job.id).desc()
    ).limit(limit).all()
    
    return {'data': [...]}
```

#### **C. Metadata Endpoints**

```python
@app.get('/api/metadata')
def get_metadata(db: Session = Depends(get_db)):
    # Trả về danh sách unique locations, levels, companies
    # Để frontend dùng cho dropdown filters
    
    locations = db.query(models.Job.location)\
                  .distinct().filter(models.Job.location != None).all()
    levels = db.query(models.Job.level)\
               .distinct().filter(models.Job.level != None).all()
    
    return {
        'locations': sorted([l[0] for l in locations]),
        'levels': sorted([l[0] for l in levels])
    }
```

---

### **5️⃣ Giai Đoạn Frontend**

#### **Module: React Frontend** (`frontend/src/`)

**Kiến trúc Component:**
```
App.tsx (Root component)
├── Dashboard Tab
│   ├── Salary Distribution Chart (Line Chart)
│   ├── Top Locations Chart (Bar Chart)
│   └── Job Level Distribution (Pie Chart)
│
├── Advanced Analytics Tab
│   ├── Statistics Cards (Total jobs, Avg salary, etc.)
│   ├── Top Skills Chart
│   ├── Company Analysis Chart
│   └── Title-Salary Insights Table
│
├── Advanced Search Tab
│   ├── Search Form (title, company, location, level, salary range)
│   ├── Results Table with sorting
│   └── Export to XLSX functionality
│
├── Top 30 Jobs Tab
│   └── High Salary Jobs List
│
├── Data Sources Tab
│   └── Market Overview & Trending Jobs
│
└── Job List Tab (Full Dataset)
    └── Paginated table with all jobs
```

#### **Luồng Hoạt Động Frontend:**

**1. Component Lifecycle:**
```typescript
function App() {
    const [salaryVals, setSalaryVals] = useState<number[]>([])
    const [byLoc, setByLoc] = useState<any[]>([])
    const [byLevel, setByLevel] = useState<any[]>([])
    
    // 1. Component mount → fetch data từ API
    useEffect(() => {
        const base = 'http://127.0.0.1:8081'
        
        // Parallel API calls
        Promise.all([
            axios.get(base + '/api/analytics/salary_distribution'),
            axios.get(base + '/api/analytics/by_location'),
            axios.get(base + '/api/analytics/by_level')
        ]).then(([salaryResp, locResp, levelResp]) => {
            setSalaryVals(salaryResp.data.values)
            setByLoc(locResp.data.data)
            setByLevel(levelResp.data.data)
        })
    }, [])
    
    // 2. Render charts with fetched data
    return (
        <Container>
            <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab label="Dashboard Cơ Bản" />
                <Tab label="Phân Tích Nâng Cao" />
                {/* ... more tabs */}
            </Tabs>
            
            {activeTab === 0 && <DashboardTab data={{salaryVals, byLoc, byLevel}} />}
            {activeTab === 1 && <AdvancedAnalytics />}
            {/* ... */}
        </Container>
    )
}
```

**2. Dashboard Charts:**
```typescript
// Salary Distribution - Line Chart
const salaryChartData = {
    labels: salaryVals.map((_, i) => `Mức ${i + 1}`),
    datasets: [{
        label: 'Lương (triệu VND)',
        data: salaryVals,
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
    }]
}

<Line data={salaryChartData} options={chartOptions} />

// Top Locations - Bar Chart
const locationChartData = {
    labels: byLoc.map(d => d.location),
    datasets: [{
        label: 'Lương TB (triệu VND)',
        data: byLoc.map(d => d.avg_salary),
        backgroundColor: 'rgba(54, 162, 235, 0.6)'
    }]
}

<Bar data={locationChartData} options={chartOptions} />
```

**3. Advanced Search Component:**
```typescript
function AdvancedSearch() {
    const [filters, setFilters] = useState({
        title: '',
        company: '',
        location: '',
        level: '',
        minSalary: '',
        maxSalary: ''
    })
    const [results, setResults] = useState([])
    
    const handleSearch = () => {
        // Build query params
        const params = new URLSearchParams()
        if (filters.title) params.append('title', filters.title)
        if (filters.location) params.append('location', filters.location)
        if (filters.minSalary) params.append('min_salary', filters.minSalary)
        // ... more params
        
        // Call API
        axios.get(`/api/jobs?${params.toString()}`)
            .then(resp => setResults(resp.data.items))
    }
    
    return (
        <Box>
            <TextField label="Job Title" value={filters.title} 
                       onChange={e => setFilters({...filters, title: e.target.value})} />
            <TextField label="Company" value={filters.company} ... />
            <Button onClick={handleSearch}>Tìm kiếm</Button>
            
            <TableContainer>
                <Table>
                    {results.map(job => (
                        <TableRow key={job.id}>
                            <TableCell>{job.title}</TableCell>
                            <TableCell>{job.company}</TableCell>
                            <TableCell>{job.avg_salary_mil_vnd} triệu</TableCell>
                        </TableRow>
                    ))}
                </Table>
            </TableContainer>
        </Box>
    )
}
```

**4. Export to Excel:**
```typescript
import * as XLSX from 'xlsx'

const handleExportExcel = () => {
    // 1. Prepare data
    const exportData = results.map(job => ({
        'Tiêu đề': job.title,
        'Công ty': job.company,
        'Địa điểm': job.location,
        'Cấp độ': job.level,
        'Lương (triệu)': job.avg_salary_mil_vnd,
        'Kỹ năng': job.skills
    }))
    
    // 2. Create worksheet
    const ws = XLSX.utils.json_to_sheet(exportData)
    
    // 3. Create workbook
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Jobs')
    
    // 4. Download file
    XLSX.writeFile(wb, 'job_search_results.xlsx')
}
```

---

## 🔐 Authentication & Authorization

```python
# backend/auth.py

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), 
                          hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post('/api/auth/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@app.post('/api/admin/add-job')
def add_job(job: JobCreate, 
            current_user: User = Depends(get_current_admin_user),
            db: Session = Depends(get_db)):
    # Only admin can add jobs
    new_job = models.Job(**job.dict())
    db.add(new_job)
    db.commit()
    return {"status": "success"}
```

---

## 📊 Data Flow Summary

```
┌──────────────┐
│   TopCV      │ ← 1. Crawl data
│   Website    │
└──────┬───────┘
       │ HTML
       ▼
┌──────────────┐
│   Crawler    │ ← 2. Parse HTML → Extract data
│  (Python)    │
└──────┬───────┘
       │ CSV (raw)
       ▼
┌──────────────┐
│   Salary     │ ← 3. Clean & normalize data
│   Parser     │
└──────┬───────┘
       │ CSV (processed)
       ▼
┌──────────────┐
│   Import     │ ← 4. Insert into database
│   Script     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   SQLite     │ ← 5. Store persistent data
│   Database   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FastAPI    │ ← 6. Expose REST API
│   Backend    │
└──────┬───────┘
       │ JSON
       ▼
┌──────────────┐
│   React      │ ← 7. Display charts & UI
│   Frontend   │
└──────────────┘
```

---

## 🎯 Các Tính Năng Nổi Bật

### 1. **Real-time Search với Multiple Filters**
- Filter theo: title, company, location, level, salary range
- Sorting theo bất kỳ column nào
- Pagination hiệu quả

### 2. **Advanced Analytics**
- Salary distribution histogram
- Top locations by average salary
- Job level distribution
- Top skills analysis
- Company hiring trends
- Title-salary correlation

### 3. **Data Visualization**
- Chart.js cho basic charts
- Recharts cho advanced charts
- Responsive design
- Interactive tooltips

### 4. **Export Functionality**
- Export search results to Excel
- Custom column selection
- Vietnamese character support

### 5. **Admin Panel** (Future Enhancement)
- Manual job entry
- Data management
- Crawler control
- User management

---

## 🛠️ Công Nghệ Sử Dụng

### Backend Stack:
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL ORM for Python
- **Pydantic**: Data validation
- **SQLite**: Lightweight database
- **BeautifulSoup4**: HTML parsing
- **Pandas**: Data processing

### Frontend Stack:
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Material-UI**: Component library
- **Chart.js**: Charting library
- **Recharts**: React charting library
- **Axios**: HTTP client
- **XLSX**: Excel export

### DevOps:
- **Vite**: Fast build tool
- **Uvicorn**: ASGI server
- **Git**: Version control

---

## 📈 Performance Optimizations

1. **Database Indexing**: Index trên title, company, location, level, avg_salary
2. **API Pagination**: Limit results per page
3. **Frontend Caching**: Cache API responses
4. **Lazy Loading**: Load components on demand
5. **SQL Query Optimization**: Use aggregation functions efficiently

---

## 🔮 Future Enhancements

1. **PostgreSQL Migration**: Scale to production database
2. **Redis Caching**: Cache frequently accessed data
3. **Job Alerts**: Email notifications for matching jobs
4. **Machine Learning**: Salary prediction models
5. **Recommendation System**: Job recommendations based on user profile
6. **Mobile App**: React Native mobile version
7. **Real-time Updates**: WebSocket for live data updates

---

## 📚 References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- SQLAlchemy ORM: https://www.sqlalchemy.org/
- Material-UI: https://mui.com/

---

**Tài liệu này được tạo để hỗ trợ trình bày báo cáo với giảng viên.**
**Ngày cập nhật: 30/01/2026**
