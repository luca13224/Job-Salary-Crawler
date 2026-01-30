# Quick Start Guide - 5 Minute Setup

## 🚀 Start the Application

### Step 1: Open Two Terminals

**Terminal 1 - Start Backend**:
```bash
cd d:\job-market-crawler-salary-analytics
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081
```

Wait for output:
```
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Terminal 2 - Start Frontend**:
```bash
cd d:\job-market-crawler-salary-analytics\frontend
npm run dev
```

Wait for output:
```
  VITE v5.4.21  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### Step 2: Open Browser
Go to: **http://localhost:5173**

You should see:
- ✅ Colorful dashboard with 8 tabs
- ✅ Charts and data visualizations
- ✅ Navigation working smoothly

---

## 🎯 Key Features to Try

### 1️⃣ View Top 30 Highest-Paying Jobs
Click tab: **"⭐ Top 30 Cao Lương"**
- See 30 jobs ranked by salary
- Gold/Silver/Bronze medals for ranks
- Salary ranges: 90M - 150M+ VND

### 2️⃣ Search Jobs with Autocomplete
Click tab: **"🔍 Tìm Kiếm Nâng Cao"**
- Type "dev" in "Chức vụ" field → See suggestions
- Type "FPT" in "Công ty" field → See company suggestions
- Type "Senior" in "Cấp độ" → See level suggestions
- Use salary slider to filter
- Click "Tìm Kiếm" to see results

### 3️⃣ Browse All Jobs
Click tab: **"💼 Danh Sách Công Việc"**
- See all 909 jobs in interactive grid
- Click column headers to sort
- Change pagination size (20, 50, 100)
- Click "Tải XLSX" to export to Excel

### 4️⃣ View Analytics
Click tab: **"🔬 Phân Tích Nâng Cao"**
- 6 professional charts using Recharts
- Salary by job level
- Top locations
- Top skills
- Company analysis
- Salary distribution
- Top job titles

### 5️⃣ Login as Admin
Click tab: **"🔐 Đăng Nhập"**
- Username: `admin`
- Password: `demo123`
- After login, click **"⚙️ Admin"** tab
- Add jobs manually or upload files

---

## 📊 Dashboard Overview

### Tab 0: Dashboard Cơ Bản (📈)
- Basic overview charts
- Salary distribution histogram
- Top locations by salary
- Jobs by level

### Tab 1: Phân Tích Nâng Cao (🔬)
- 6 advanced analytics charts
- Interactive Recharts visualizations
- Deep market insights

### Tab 2: Top 30 Cao Lương (⭐) **NEW**
- Top 30 highest-paying jobs
- Visual ranking badges
- Skill requirements for each job

### Tab 3: Nguồn Dữ liệu (📡)
- Market overview KPIs
- Data source breakdown
- Trending jobs (last 30 days)
- Top locations map

### Tab 4: Tìm Kiếm Nâng Cao (🔍)
- Multi-field search
- Autocomplete suggestions
- Salary range filter
- Real-time results

### Tab 5: Danh Sách Công Việc (💼)
- All 909 jobs in DataGrid
- Sortable columns
- Paginated (20-100 per page)
- Excel export
- Search by title

### Tab 6: Admin (⚙️) - *After login*
- Add new jobs
- Upload job files
- Run crawler
- View system logs

### Tab 7: Đăng Nhập / Đăng Xuất (🔐)
- Admin authentication
- Login: admin / demo123
- Logout button after login

---

## ⌨️ Keyboard Shortcuts

- `Tab` - Navigate between tabs
- `Ctrl+F` - Browser search
- `Ctrl+Shift+I` - Developer console (for debugging)
- `Ctrl+K` - Search in table (if available)

---

## 🐛 Quick Troubleshooting

### "Connection Refused" Error
```
Solution: Restart the backend server
cd d:\job-market-crawler-salary-analytics
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081
```

### Autocomplete Not Showing
```
Solution: 
1. Type slowly (debounce is 300ms)
2. Type at least 1 character
3. Check browser console (F12) for errors
4. Refresh page (Ctrl+F5)
```

### Admin Tab Not Visible
```
Solution:
1. Login first (admin / demo123)
2. Page should refresh
3. Admin tab should appear
4. If not, check browser console
```

### Excel Export Not Working
```
Solution:
1. Click "Tải XLSX" button
2. File should download in a few seconds
3. Check Downloads folder
4. Try again with fewer jobs (use search filter first)
```

---

## 📱 Mobile Testing

The app is fully responsive:
- Desktop: 2 columns in grids
- Tablet: 1-2 columns
- Mobile: Single column, full width

Test by pressing `F12` in browser and clicking mobile icon (top-left of DevTools).

---

## 🔗 Useful URLs

| Page | URL |
|------|-----|
| **Main App** | http://localhost:5173 |
| **API Docs** | http://127.0.0.1:8081/docs (Swagger) |
| **Jobs API** | http://127.0.0.1:8081/api/jobs |
| **Top 30 Jobs** | http://127.0.0.1:8081/api/analytics/top-30-jobs |
| **Analytics** | http://127.0.0.1:8081/api/analytics/* |

---

## 💡 Pro Tips

1. **Export Data**: Use "💼 Danh Sách Công Việc" tab → "Tải XLSX" to get all jobs in Excel
2. **Find Specific Jobs**: Use "🔍 Tìm Kiếm Nâng Cao" with multiple filters
3. **Salary Insights**: Check "⭐ Top 30 Cao Lương" to see market leaders
4. **Market Trends**: View "📡 Nguồn Dữ liệu" for data source breakdown
5. **Admin Features**: After login, click "⚙️ Admin" to add/manage jobs

---

## ❓ FAQ

**Q: Where does the data come from?**
A: 909 jobs imported from CSV/TopCV crawler. Located in `data/jobs.db`

**Q: Can I add more jobs?**
A: Yes! Click "⚙️ Admin" tab → "Thêm Job" button (requires login: admin/demo123)

**Q: Why is my autocomplete dropdown not showing?**
A: Check the browser console (F12) for errors. The endpoint is working but MUI config may need adjustment.

**Q: How do I reset the database?**
A: Delete `data/jobs.db` and restart the backend. It will create a new database with 909 jobs.

**Q: Can I change the password?**
A: Edit `backend/main.py`, find the admin user setup, and change the password hash. Requires backend restart.

**Q: How do I export all jobs?**
A: Go to "💼 Danh Sách Công Việc" → Click "Tải XLSX" → Excel file downloads

---

## ✅ Pre-Demo Checklist

Before showing to stakeholders:
- [ ] Both servers are running (backend + frontend)
- [ ] Browser loads http://localhost:5173 without errors
- [ ] All 8 tabs visible and clickable
- [ ] Charts load with data
- [ ] Search autocomplete working
- [ ] Export to Excel working
- [ ] Admin login working (admin/demo123)
- [ ] Mobile view responsive

---

**Ready to start?**
Just run the two server commands above and open http://localhost:5173 in your browser! 🎉

Questions? Check SETUP_GUIDE.md or TESTING_CHECKLIST.md for detailed info.
