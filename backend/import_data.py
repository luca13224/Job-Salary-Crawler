import pandas as pd
import glob
import os
from .database import SessionLocal, engine, Base
from . import models

Base.metadata.create_all(bind=engine)

def import_processed_csvs(processed_dir=os.path.join('data', 'processed')):
    files = glob.glob(os.path.join(processed_dir, '*.csv'))
    if not files:
        print('No processed CSV files found in', processed_dir)
        return 0
    db = SessionLocal()
    inserted = 0
    try:
        # optional: clear table for fresh import
        # db.query(models.Job).delete()
        for f in files:
            print('Importing', f)
            df = pd.read_csv(f)
            # normalize column names
            if 'job_title' in df.columns and 'title' not in df.columns:
                df.rename(columns={'job_title': 'title'}, inplace=True)
            # ensure avg_salary_mil_vnd exists
            if 'avg_salary_mil_vnd' not in df.columns and 'salary' in df.columns:
                # simple parse: take first number
                df['avg_salary_mil_vnd'] = df['salary'].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
            for _, row in df.iterrows():
                job = models.Job(
                    title=row.get('title'),
                    company=row.get('company', ''),
                    level=row.get('level', ''),
                    salary_raw=row.get('salary', ''),
                    avg_salary_mil_vnd=float(row.get('avg_salary_mil_vnd')) if not pd.isna(row.get('avg_salary_mil_vnd')) else None,
                    location=row.get('location', ''),
                    skills=row.get('skills', ''),
                    source=row.get('source', ''),
                    url=row.get('url', ''),
                    crawled_at=row.get('crawled_at', '')
                )
                db.add(job)
                inserted += 1
            db.commit()

        # Ensure admin user exists for demo
        admin = db.query(models.User).filter(models.User.username == 'admin').first()
        if not admin:
            from .auth import get_password_hash
            u = models.User(username='admin', hashed_password=get_password_hash('demo123'), role='admin')
            db.add(u)
            db.commit()
            print('Created default admin (username: admin, password: demo123)')

        # Ensure settings row exists
        settings = db.query(models.AdminSetting).first()
        if not settings:
            s = models.AdminSetting(crawl_enabled=1)
            db.add(s)
            db.commit()
            print('Initialized admin settings')

    finally:
        db.close()
    print(f'Imported {inserted} rows')
    return inserted

if __name__ == '__main__':
    import_processed_csvs()
