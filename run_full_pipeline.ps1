# PowerShell Script - Crawl và import dữ liệu thật từ TopCV
# Chạy: .\run_full_pipeline.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 TopCV Real Data Collection & Import Pipeline" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Crawl data from TopCV
Write-Host "📡 Step 1/3: Crawling job data from TopCV..." -ForegroundColor Yellow
python src/crawler/topcv_crawler.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Crawler failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Crawling completed!" -ForegroundColor Green
Write-Host ""

# Step 2: Process salary data
Write-Host "⚙️  Step 2/3: Processing salary data..." -ForegroundColor Yellow
python src/processing/salary_parser.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Processing failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Processing completed!" -ForegroundColor Green
Write-Host ""

# Step 3: Import to database
Write-Host "💾 Step 3/3: Importing to database..." -ForegroundColor Yellow
python import_to_db.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Import failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✨ All done! Real data from TopCV is now in your database!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 You can now:" -ForegroundColor White
Write-Host "   • Refresh your web app at http://localhost:5174" -ForegroundColor White
Write-Host "   • View real job market analytics with actual TopCV data" -ForegroundColor White
Write-Host ""
