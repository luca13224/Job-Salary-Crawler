# Testing Checklist - Job Market Analytics Platform

## ✅ System Status Check

### Backend
- [ ] Port 8081 is listening: `netstat -ano | findstr :8081`
- [ ] Uvicorn shows "Application startup complete"
- [ ] No error messages in backend terminal

### Frontend
- [ ] Port 5173 is listening
- [ ] Vite shows "ready in xxx ms"
- [ ] Browser loads http://localhost:5173 without errors

### Database
- [ ] File exists: `data/jobs.db`
- [ ] Contains 909 jobs (verify with Admin Panel)

---

## 🧪 Functional Tests

### Tab 1: Dashboard (📈 Dashboard Cơ Bản)
- [ ] Page loads without errors
- [ ] Shows 3 charts: "Phân Bố Lương", "Top Địa Điểm", "Theo Cấp Độ"
- [ ] Charts display data (not empty)
- [ ] Responsive on mobile view

### Tab 2: Advanced Analytics (🔬 Phân Tích Nâng Cao)
- [ ] Page loads without errors
- [ ] Shows 6 Recharts-based charts
- [ ] Charts include: Salary by Level, Top Locations, Top Skills, Companies, Distribution, Top Titles
- [ ] All charts are interactive (hover shows values)
- [ ] Charts load data from `/api/analytics/*` endpoints

### Tab 3: Top 30 Jobs (⭐ Top 30 Cao Lương) **NEW**
- [ ] Page loads and shows "Top 30 Công Việc Cao Lương"
- [ ] Shows exactly 30 or fewer job cards in grid layout
- [ ] Each card displays:
  - [ ] Rank number (1-30) with medal color (Gold #1-10, Silver #11-20, Bronze #21-30)
  - [ ] Job title + company name (blue text)
  - [ ] Salary in millions (green, bold)
  - [ ] Level, location, source chips
  - [ ] 3-5 skill chips with +N indicator
  - [ ] Crawl date + "Xem chi tiết" link
- [ ] Grid is responsive (1 column on mobile, 2 on desktop)
- [ ] Loading spinner appears while fetching
- [ ] Error message shown if API fails

### Tab 4: Data Sources (📡 Nguồn Dữ liệu)
- [ ] Page loads without errors
- [ ] Shows 4 KPI cards at top:
  - [ ] "Tổng công việc": Shows 909 (or current count)
  - [ ] "Có lương": Shows jobs with salary data
  - [ ] "Hoàn chỉnh %": Shows data completeness
  - [ ] "Nguồn dữ liệu": Shows number of sources
- [ ] Pie chart shows "Công Việc Theo Nguồn" (jobs by source)
- [ ] Bar chart shows "Top 5 Địa Điểm" 
- [ ] "Công Việc Mới (30 ngày)" section shows recent jobs
- [ ] Loading states work properly

### Tab 5: Advanced Search (🔍 Tìm Kiếm Nâng Cao)
- [ ] Page loads with search form
- [ ] **Autocomplete Fields** (THIS IS THE KEY TEST):
  - [ ] **Chức vụ** (Title): Type "dev" → autocomplete suggestions appear
  - [ ] **Công ty** (Company): Type "FPT" → suggestions appear
  - [ ] **Địa điểm** (Location): Type "Hà" → suggestions appear
  - [ ] **Cấp độ** (Level): Type "Senior" → suggestions appear
  - [ ] **Kỹ năng** (Skills): Type "Java" → suggestions appear
- [ ] Search button triggers filtering
- [ ] Results display in DataGrid below
- [ ] Salary slider works (min-max filtering)
- [ ] "✓ Tìm thấy X kết quả" summary card appears

### Tab 6: Job List (💼 Danh Sách Công Việc)
- [ ] DataGrid loads with all 909 jobs
- [ ] **Columns visible**: ID, Chức vụ, Công ty, Cấp độ, Lương, Địa điểm
- [ ] **Sorting works**: Click column header to sort
- [ ] **Pagination works**: Change rows per page (20, 50, 100)
- [ ] **Title autocomplete search**: Type in search box → suggestions appear
- [ ] **Export button**: "Tải XLSX" exports data to Excel file
- [ ] Each skill displays as chip with max 3 visible + "+..." indicator
- [ ] Mobile responsive (horizontal scroll)

### Tab 7: Admin Panel (⚙️ Admin) - *Visible only after login*
- [ ] Login first with: admin / demo123
- [ ] After login, Admin tab appears in tabs
- [ ] Admin panel shows:
  - [ ] "Tải File" section (file upload for jobs)
  - [ ] "Chạy Crawler" button (crawler controls)
  - [ ] "Thêm Job" button (opens add job modal)
  - [ ] System logs display (shows recent API calls)
- [ ] **Add Job Modal** (click "Thêm Job"):
  - [ ] Form has fields: Title, Company, Level, Salary, Location, Skills, Source, URL
  - [ ] Submit button works and adds job to database
- [ ] Logs refresh every 30 seconds

### Tab 8: Login (🔐 Đăng Nhập) or Logout (🚪 Đăng Xuất)
- [ ] **Before Login**:
  - [ ] Tab label shows "🔐 Đăng Nhập"
  - [ ] Form has fields: Username, Password
  - [ ] Error message for wrong credentials
  - [ ] Enter admin/demo123:
    - [ ] JWT token stored in localStorage
    - [ ] Tab label changes to "🚪 Đăng Xuất"
    - [ ] Admin tab becomes visible
    - [ ] Page redirects to Admin Panel (or shows success)
- [ ] **After Login**:
  - [ ] Tab label shows "🚪 Đăng Xuất"
  - [ ] Click logout:
    - [ ] Token removed from localStorage
    - [ ] Tab label changes back to "🔐 Đăng Nhập"
    - [ ] Admin tab disappears
    - [ ] User redirected to Dashboard

---

## 🔌 API Endpoint Tests

Use Python/curl to test endpoints. Example:
```python
import requests

base = 'http://127.0.0.1:8081'

# Test Jobs endpoint
resp = requests.get(f'{base}/api/jobs?page=1&per_page=5')
assert resp.status_code == 200
assert len(resp.json()['items']) > 0
print(f"✓ Jobs endpoint working, found {resp.json()['total']} jobs")

# Test Top 30 endpoint
resp = requests.get(f'{base}/api/analytics/top-30-jobs')
assert resp.status_code == 200
assert len(resp.json()) <= 30
print(f"✓ Top 30 endpoint working, found {len(resp.json())} jobs")

# Test Suggestions endpoint
resp = requests.get(f'{base}/api/suggestions/titles?q=dev&limit=5')
assert resp.status_code == 200
assert 'suggestions' in resp.json()
print(f"✓ Suggestions endpoint working")
```

### Critical Endpoints to Test:
- [ ] `GET /api/jobs` - Should return jobs with pagination
- [ ] `GET /api/analytics/top-30-jobs` - Should return array of 30 or fewer jobs
- [ ] `GET /api/suggestions/titles?q=dev` - Should return title suggestions
- [ ] `GET /api/suggestions/companies?q=fpt` - Should return company suggestions
- [ ] `GET /api/suggestions/locations?q=ha` - Should return location suggestions
- [ ] `POST /api/auth/login` - Should return JWT token for admin/demo123

---

## 🐛 Known Issues & Solutions

### Issue 1: Autocomplete Dropdown Not Visible
**Symptom**: Type in search field but no dropdown appears
**Solution**:
1. Check browser developer console (F12) for errors
2. Verify `/api/suggestions/titles` endpoint returns data
3. Check if MUI Autocomplete component needs `open` state management
4. Try typing slowly - debounce is set to 300ms

### Issue 2: Backend Not Responding
**Symptom**: "Failed to connect to http://127.0.0.1:8081"
**Solution**:
1. Verify uvicorn is still running: `netstat -ano | findstr :8081`
2. Check backend terminal for error messages
3. Restart backend: `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081`

### Issue 3: Top 30 Tab Not Showing
**Symptom**: Only 7 tabs visible, no "⭐ Top 30 Cao Lương" tab
**Solution**:
1. Frontend may not have hot-reloaded
2. Try hard refresh (Ctrl+F5) in browser
3. Restart frontend server (Ctrl+C then `npm run dev`)

### Issue 4: Pydantic Warning on Startup
**Message**: "Valid config keys have changed in V2: 'orm_mode' has been renamed to 'from_attributes'"
**Solution**: This is just a warning, system still works. To fix:
1. Open `backend/models.py`
2. Find `class Config: orm_mode = True`
3. Change to `class Config: from_attributes = True`

### Issue 5: Login Not Working
**Symptom**: "Invalid credentials" even with admin/demo123
**Solution**:
1. Check if `/api/auth/login` endpoint is working
2. Verify admin user exists in database
3. Clear localStorage and try again
4. Check backend logs for error details

---

## 📊 Expected Data Samples

### Top 30 Jobs Sample (First 3):
```json
[
  {
    "id": 1,
    "title": "Senior Backend Developer",
    "company": "FPT Software",
    "level": "Senior",
    "salary": 120.5,
    "location": "Ho Chi Minh City",
    "skills": "Python,Django,PostgreSQL",
    "source": "TopCV",
    "url": "https://...",
    "crawled_at": "2025-01-15T10:30:00"
  },
  {
    "id": 2,
    "title": "Principal Engineer",
    "company": "Viet Tech Corp",
    "level": "Principal",
    "salary": 150.0,
    "location": "Hanoi",
    "skills": "Go,Kubernetes,CI/CD",
    "source": "LinkedIn",
    "url": "https://...",
    "crawled_at": "2025-01-14T14:20:00"
  },
  ...
]
```

### Suggestions Sample:
```json
{
  "suggestions": [
    "Backend Developer",
    "Frontend Developer",
    "Fullstack Developer",
    "Mobile Developer",
    "DevOps Engineer"
  ]
}
```

---

## ✨ Performance Benchmarks

- [ ] Dashboard loads in < 2 seconds
- [ ] Top 30 loads in < 1.5 seconds
- [ ] Search with autocomplete in < 0.5 seconds (300ms debounce)
- [ ] DataGrid with 909 rows renders smoothly
- [ ] Export XLSX completes in < 5 seconds
- [ ] No memory leaks (check browser DevTools)

---

## 📝 Final Validation

Before marking as complete:

- [ ] All 8 tabs are visible and labeled correctly
- [ ] All tabs load without errors
- [ ] Autocomplete suggestions appear when typing
- [ ] DataGrid is fully functional with sorting/pagination
- [ ] Admin panel accessible after login (admin/demo123)
- [ ] No error messages in browser console
- [ ] No error messages in backend terminal
- [ ] Responsive on mobile devices (test with browser DevTools mobile mode)

---

**Testing Date**: ___________
**Tester Name**: ___________
**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

**Notes**:
_________________________________
_________________________________
_________________________________
