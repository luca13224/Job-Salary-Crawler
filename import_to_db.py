"""
Script để import dữ liệu thật từ crawler vào database
Tên dataset: "TopCV IT Jobs - Real Market Data"
"""
import pandas as pd
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.database import engine, SessionLocal
from backend import models

def clear_existing_data(session):
    """Xóa dữ liệu cũ (fake data) trong database"""
    print("🗑️  Clearing old data...")
    deleted = session.query(models.Job).delete()
    session.commit()
    print(f"   Deleted {deleted} old records")

def import_from_csv(csv_path, session, dataset_name="TopCV IT Jobs - Real Market Data"):
    """Import dữ liệu từ file CSV đã được process vào database"""
    print(f"\n📥 Importing data from: {csv_path}")
    print(f"   Dataset name: {dataset_name}")
    
    df = pd.read_csv(csv_path)
    print(f"   Found {len(df)} job records")
    
    imported = 0
    skipped = 0
    
    for idx, row in df.iterrows():
        try:
            # Ưu tiên level từ data, fallback sang extract từ title
            level = row.get('level') if 'level' in row and pd.notna(row.get('level')) else extract_level(row.get('title', ''))
            
            job = models.Job(
                title=str(row.get('title', 'N/A')),
                company=str(row.get('company', 'Unknown')),
                location=str(row.get('location', 'N/A')),
                level=str(level),
                salary_raw=str(row.get('salary', 'Thỏa thuận')),  # Sửa: salary_text -> salary_raw
                avg_salary_mil_vnd=pd.to_numeric(row.get('avg_salary_mil_vnd'), errors='coerce'),
                url=str(row.get('url', '')),
                skills=str(row.get('skills', '')),
                source=dataset_name,  # Đặt tên dataset
                crawled_at=datetime.now().isoformat()
            )
            session.add(job)
            imported += 1
            
            if imported % 100 == 0:
                session.commit()
                print(f"   Imported {imported} jobs...")
                
        except Exception as e:
            print(f"   ⚠️  Error importing row {idx}: {e}")
            skipped += 1
            continue
    
    session.commit()
    print(f"\n✅ Import completed!")
    print(f"   • Imported: {imported} jobs")
    print(f"   • Skipped: {skipped} jobs")
    return imported

def extract_level(title):
    """Extract job level từ title"""
    title_lower = str(title).lower()
    if any(word in title_lower for word in ['intern', 'thực tập']):
        return 'Intern'
    elif any(word in title_lower for word in ['senior', 'sr', 'lead', 'principal']):
        return 'Senior'
    elif any(word in title_lower for word in ['junior', 'jr', 'fresher']):
        return 'Junior'
    elif any(word in title_lower for word in ['manager', 'director', 'head']):
        return 'Manager'
    elif any(word in title_lower for word in ['mid', 'middle']):
        return 'Mid-level'
    else:
        return 'Mid-level'  # Default

def get_latest_processed_file():
    """Tìm file processed mới nhất"""
    import glob
    processed_dir = 'data/processed'
    files = glob.glob(os.path.join(processed_dir, 'processed_*.csv'))
    if not files:
        return None
    return max(files, key=os.path.getctime)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 TopCV Real Data Importer")
    print("=" * 60)
    
    # Tìm file processed mới nhất
    latest_file = get_latest_processed_file()
    
    if not latest_file:
        print("❌ No processed data found!")
        print("   Please run these commands first:")
        print("   1. python src/crawler/topcv_crawler.py  (to crawl data)")
        print("   2. python src/processing/salary_parser.py  (to process data)")
        sys.exit(1)
    
    print(f"\n📂 Found processed file: {os.path.basename(latest_file)}")
    
    # Confirm
    response = input("\n⚠️  This will replace ALL existing data. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Import cancelled")
        sys.exit(0)
    
    # Create session
    session = SessionLocal()
    
    try:
        # Clear old data
        clear_existing_data(session)
        
        # Import new data
        dataset_name = f"TopCV IT Jobs - Real Data ({datetime.now().strftime('%Y-%m-%d')})"
        imported = import_from_csv(latest_file, session, dataset_name)
        
        print(f"\n{'=' * 60}")
        print(f"✨ Successfully imported {imported} real jobs from TopCV!")
        print(f"{'=' * 60}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()
