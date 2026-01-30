#!/bin/bash
# Script tổng hợp để crawl và import dữ liệu thật từ TopCV vào database

echo "============================================================"
echo "🚀 TopCV Real Data Collection & Import Pipeline"
echo "============================================================"
echo ""

# Step 1: Crawl data from TopCV
echo "📡 Step 1/3: Crawling job data from TopCV..."
python src/crawler/topcv_crawler.py
if [ $? -ne 0 ]; then
    echo "❌ Crawler failed!"
    exit 1
fi

echo ""
echo "✅ Crawling completed!"
echo ""

# Step 2: Process salary data
echo "⚙️  Step 2/3: Processing salary data..."
python src/processing/salary_parser.py
if [ $? -ne 0 ]; then
    echo "❌ Processing failed!"
    exit 1
fi

echo ""
echo "✅ Processing completed!"
echo ""

# Step 3: Import to database
echo "💾 Step 3/3: Importing to database..."
python import_to_db.py
if [ $? -ne 0 ]; then
    echo "❌ Import failed!"
    exit 1
fi

echo ""
echo "============================================================"
echo "✨ All done! Real data from TopCV is now in your database!"
echo "============================================================"
echo ""
echo "🌐 You can now:"
echo "   • Refresh your web app at http://localhost:5174"
echo "   • View real job market analytics with actual TopCV data"
echo ""
