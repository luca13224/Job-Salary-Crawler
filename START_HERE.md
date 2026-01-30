# 🚀 START HERE - Immediate Action Guide

## ⏰ 2-Minute Quick Setup

### Step 1: Open Terminal 1 (Backend)
```bash
cd d:\job-market-crawler-salary-analytics
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081
```
**Wait for**: `Application startup complete.`

### Step 2: Open Terminal 2 (Frontend)
```bash
cd d:\job-market-crawler-salary-analytics\frontend
npm run dev
```
**Wait for**: `Local: http://localhost:5173/`

### Step 3: Open Browser
Go to: **http://localhost:5173**

✅ **Done!** Your application is running.

---

## 🎮 What You Can Do Right Now

| Action | Tab | How |
|--------|-----|-----|
| **View Top 30** | Click "⭐ Top 30 Cao Lương" | See highest-paying jobs |
| **Search Jobs** | Click "🔍 Tìm Kiếm Nâng Cao" | Type "dev" to see suggestions |
| **Browse All** | Click "💼 Danh Sách Công Việc" | See 909 jobs, sort, export |
| **Analytics** | Click "🔬 Phân Tích Nâng Cao" | See 6 professional charts |
| **Login** | Click "🔐 Đăng Nhập" | admin / demo123 |
| **Admin** | Click "⚙️ Admin" (after login) | Manage jobs, view logs |

---

## ❓ Problem? Quick Fixes

### Autocomplete Not Showing
```
✓ Type slowly in search box
✓ Check browser console (F12)
✓ Try Ctrl+F5 (hard refresh)
```

### Backend Not Found
```
✓ Make sure Terminal 1 still running
✓ Check for "Application startup complete"
✓ Try restarting: Ctrl+C then run again
```

### Frontend Not Loading
```
✓ Make sure Terminal 2 still running
✓ Check for "ready in xxx ms"
✓ Try hard refresh (Ctrl+F5)
```

### Admin Tab Missing
```
✓ Login first with admin/demo123
✓ Check that login succeeded
✓ Refresh page if needed
```

---

## 📚 Documentation Files

Read these for more info:

| File | For |
|------|-----|
| **QUICKSTART.md** | Detailed 5-min setup |
| **SETUP_GUIDE.md** | Full installation guide |
| **TESTING_CHECKLIST.md** | Testing all features |
| **COMPLETION_SUMMARY.md** | What's been completed |
| **CHANGES.md** | Recent updates |

---

## ✨ Features Overview

### 8 Main Tabs

1. **📈 Dashboard** → Basic salary charts
2. **🔬 Analytics** → 6 interactive charts
3. **⭐ Top 30** → Highest-paying jobs (NEW!)
4. **📡 Sources** → Market overview
5. **🔍 Search** → Smart search + autocomplete
6. **💼 Jobs** → 909 jobs, sort, export
7. **⚙️ Admin** → Manage jobs (login required)
8. **🔐 Login** → Authentication

---

## 🎯 Demo Script (5 Minutes)

1. **Start servers** (2 min setup)
2. **Show Dashboard** (30 sec) - "See basic charts"
3. **Show Top 30** (30 sec) - "See top-paying jobs with medals"
4. **Demo Search** (1 min) - Type "dev" → show autocomplete
5. **Export Data** (30 sec) - "Get jobs as Excel"
6. **Login & Admin** (1 min) - "Show admin controls"

---

## 🔑 Credentials

**Login**: `admin`  
**Password**: `demo123`

---

## 📊 Data Stats

- **909 Jobs** in database
- **Salary Range**: 0-150M VND
- **18 API Endpoints**
- **8 React Components**
- **15+ Charts**

---

## ✅ Verification

Quick check everything works:

- [ ] Backend running on 8081 → `netstat -ano | findstr :8081`
- [ ] Frontend running on 5173 → Open http://localhost:5173
- [ ] 8 tabs visible and clickable
- [ ] Top 30 tab shows jobs with medals
- [ ] Search suggestions work when typing
- [ ] DataGrid shows 909 jobs
- [ ] Admin accessible after login (admin/demo123)

---

## 🎉 Success!

When all checks pass, you have a fully working **Job Market Analytics Platform** with:

✅ Professional UI  
✅ 909 pre-loaded jobs  
✅ Smart search  
✅ Advanced analytics  
✅ Top 30 rankings  
✅ Admin system  
✅ Mobile responsive  
✅ Excel export  

---

## 🆘 Need Help?

1. **Check browser console** (F12)
2. **Check backend terminal** for errors
3. **Check frontend terminal** for errors
4. **Read SETUP_GUIDE.md** for detailed help
5. **Try hard refresh** (Ctrl+F5)

---

## 🚀 Ready?

```bash
# Terminal 1:
cd d:\job-market-crawler-salary-analytics
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8081

# Terminal 2:
cd d:\job-market-crawler-salary-analytics\frontend
npm run dev

# Browser:
http://localhost:5173
```

**Go! 🎯**
