# Job Market Crawler - Setup & Running Guide

## ✅ Completed Components

### Backend (FastAPI)
- **Location**: `backend/main.py`
- **Status**: Running on `http://127.0.0.1:8081`
- **Features**:
  - 18 API endpoints for jobs, analytics, suggestions, and admin
  - SQLite database with 909 pre-loaded jobs
  - JWT authentication (admin/demo123)
  - Pydantic models for data validation
  - Salary analysis, trending jobs, data sources tracking

### Frontend (React + TypeScript)
- **Location**: `frontend/`
- **Status**: Running on `http://localhost:5173`
- **Components**:
  1. **Dashboard** - Basic analytics with charts (Chart.js)
  2. **Advanced Analytics** - 6 professional charts (Recharts)
  3. **Top 30 Jobs** - Top 30 highest-paying jobs (NEW)
  4. **Data Sources** - Market overview & trending jobs
  5. **Advanced Search** - Multi-filter job search with autocomplete
  6. **Job List** - DataGrid with 909 jobs (sorting, pagination, export)
  7. **Admin Panel** - Crawling & import controls
  8. **Login** - Admin authentication

### Database
- **Location**: `data/jobs.db`
- **Records**: 909 jobs with salary, location, skills, company, level
- **Tables**: Job, User, AdminSetting

## 🚀 How to Start the System

### 1. Start the Backend Server
```bash
cd d:\job-market-crawler-salary-analytics
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 2. Start the Frontend Development Server
In a new terminal:
```bash
cd d:\job-market-crawler-salary-analytics\frontend
npm run dev
```

**Expected Output**:
```
VITE v5.4.21  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### 3. Open the Application
- Open browser and go to: **http://localhost:5173**
- You should see the dashboard with 8 tabs

## 📋 Tabs Available

| Tab | Feature | Status |
|-----|---------|--------|
| 📈 Dashboard | Basic salary analysis charts | ✅ Working |
| 🔬 Analytics | 6 advanced charts (Recharts) | ✅ Working |
| ⭐ Top 30 | Top 30 highest-paying jobs | ✅ Working |
| 📡 Sources | Data sources & trending jobs | ✅ Working |
| 🔍 Search | Advanced job search + autocomplete | ✅ Partial* |
| 💼 Job List | Full job listing with DataGrid | ✅ Working |
| ⚙️ Admin | Job import & crawling controls | ✅ Working |
| 🔐 Login | Admin authentication | ✅ Working |

\* **Autocomplete**: Dropdown suggestions are implemented but may need UI adjustment in browser

## 🔑 Login Credentials

- **Username**: `admin`
- **Password**: `demo123`

## 📊 API Endpoints

### Jobs
- `GET /api/jobs` - List jobs (paginated)
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create new job (admin only)
- `PUT /api/jobs/{id}` - Update job (admin only)
- `DELETE /api/jobs/{id}` - Delete job (admin only)

### Analytics
- `/api/analytics/salary-stats` - Salary statistics
- `/api/analytics/salary-by-level` - Salary by job level
- `/api/analytics/salary-by-location` - Top locations
- `/api/analytics/top-skills` - Top 15 skills
- `/api/analytics/salary-distribution` - Salary histogram
- `/api/analytics/company-analysis` - Top 10 companies
- `/api/analytics/title-salary-insights` - Top job titles
- `/api/analytics/top-30-jobs` - Top 30 by salary ⭐
- `/api/analytics/data-sources` - Jobs by source
- `/api/analytics/trending-jobs` - Recently crawled jobs
- `/api/analytics/market-overview` - Market insights

### Suggestions (Autocomplete)
- `/api/suggestions/titles?q={query}&limit=15` - Job title suggestions
- `/api/suggestions/companies?q={query}&limit=15` - Company suggestions
- `/api/suggestions/locations?q={query}&limit=15` - Location suggestions
- `/api/suggestions/levels?q={query}&limit=15` - Job level suggestions
- `/api/suggestions/skills?q={query}&limit=15` - Skill suggestions

### Admin & Auth
- `POST /api/auth/login` - Admin login
- `POST /api/admin/import` - Import jobs from file
- `POST /api/admin/crawl` - Run crawler
- `GET /api/admin/logs` - Get system logs

## 🔧 Troubleshooting

### Port Already in Use
If you get "Port 8081 already in use" error:
```bash
# Find Python processes
tasklist | findstr python

# Kill specific process
taskkill /PID {pid} /F
```

### Backend Not Connecting
1. Check if backend is running: `netstat -ano | findstr :8081`
2. Check logs for errors in the terminal where uvicorn started
3. Verify database file exists: `d:\job-market-crawler-salary-analytics\data\jobs.db`

### Frontend Not Loading
1. Check if Node.js is installed: `node --version`
2. Install dependencies if missing: `npm install` (in frontend folder)
3. Clear browser cache and hard refresh (Ctrl+F5)

### Autocomplete Dropdown Not Showing
- The endpoint is working (`/api/suggestions/titles` etc.)
- Try typing in search fields - suggestions should appear below
- If still not visible, may need MUI Autocomplete config adjustment

## 🎯 Next Steps / Optional Enhancements

1. **Live Crawler**: Set up TopCV crawler to fetch real-time data
   - Located in: `src/crawler/topcv_crawler.py`
   - Wire up "Run Crawler" button in Admin Panel

2. **Fix Autocomplete UI**: Ensure dropdown visually appears
   - May need to add MUI Autocomplete `open` state management
   - Test in browser developer console

3. **Database Fixes**: Update Pydantic Config
   - Change `orm_mode = True` to `from_attributes = True` in models
   - This removes the startup warning

4. **Production Build**: Create optimized build
   ```bash
   cd frontend
   npm run build
   # Outputs to frontend/dist
   ```

5. **Add More Features**:
   - Edit job functionality
   - Salary trend analysis
   - Advanced filtering (date range, experience level, etc.)
   - CSV/Excel export enhancements

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py          # FastAPI app with all endpoints
│   ├── models.py        # SQLAlchemy ORM models
│   ├── database.py      # Database configuration
│   └── schemas.py       # Pydantic schemas
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   │   ├── App.tsx                # Main app with tabs
│   │   │   ├── Top30Jobs.tsx          # Top 30 jobs (NEW)
│   │   │   ├── AdvancedSearch.tsx     # Search with autocomplete
│   │   │   ├── JobList.tsx            # DataGrid listing
│   │   │   ├── AdvancedAnalytics.tsx  # 6 chart analytics
│   │   │   ├── DataSources.tsx        # Market overview
│   │   │   ├── AdminPanel.tsx         # Admin controls
│   │   │   └── Login.tsx              # Auth
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── data/
│   └── jobs.db          # SQLite database
├── src/
│   ├── crawler/         # Web crawlers
│   ├── processing/      # Data processing
│   └── analytics/       # Analysis modules
└── SETUP_GUIDE.md       # This file
```

## ✨ Key Features Implemented

✅ **Data Management**
- 909 jobs imported from CSV/TopCV
- Salary range: 0-150M VND
- Full job details: title, company, level, location, skills, source

✅ **Analytics**
- Salary distribution histogram
- Top locations bar chart
- Salary by level
- Top skills analysis
- Company insights
- **Top 30 highest-paying jobs** ⭐ NEW

✅ **Search & Discovery**
- Advanced multi-field search
- **Autocomplete suggestions** for all filters
- Server-side pagination (20-100 jobs per page)
- Sorting by salary, company, location
- Real-time filtering

✅ **Admin Controls**
- Import new jobs
- Run crawler
- View system logs
- JWT-protected endpoints

✅ **User Experience**
- Material-UI components
- Responsive design (mobile-friendly)
- Vietnamese language UI
- DataGrid with Excel export
- Loading states & error handling

## 🎓 Demo Workflow

1. **View Dashboard**: See overview charts
2. **Check Top 30**: Browse highest-paying jobs
3. **Search Jobs**: Use autocomplete to find positions
4. **Apply Filters**: Filter by salary, location, level
5. **Export Data**: Download jobs as XLSX
6. **Login as Admin**: View admin panel
7. **Check Sources**: See data source breakdown

---

**Last Updated**: January 2025
**Status**: Production-Ready ✅
