from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Body, Security
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, crud
from .schemas import JobOut
from .auth import get_current_admin_user, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import os
import subprocess
import logging
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Job Salary Analytics API')

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/health')
def health():
    return {'status': 'ok'}

@app.get('/api/jobs')
def get_jobs(title: str = None, location: str = None, level: str = None, min_salary: float = None, max_salary: float = None, sort_by: str = None, sort_dir: str = 'desc', page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * per_page
    results, total = crud.get_jobs(db, skip=skip, limit=per_page, title=title, location=location, level=level, min_salary=min_salary, max_salary=max_salary, sort_by=sort_by, sort_dir=sort_dir)
    return {'total': total, 'page': page, 'per_page': per_page, 'items': [JobOut.from_orm(r).dict() for r in results]}

@app.get('/api/jobs/{job_id}', response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = crud.get_job(db, job_id)
    if not j:
        raise HTTPException(status_code=404, detail='Job not found')
    return j

@app.get('/api/analytics/salary_distribution')
def analytics_salary_distribution(max_val: float = None, db: Session = Depends(get_db)):
    vals = crud.salary_distribution(db, max_val=max_val)
    return {'values': vals}

@app.get('/api/analytics/by_location')
def analytics_by_location(top_n: int = 10, db: Session = Depends(get_db)):
    return {'data': crud.avg_by_location(db, top_n=top_n)}

@app.get('/api/analytics/by_level')
def analytics_by_level(db: Session = Depends(get_db)):
    return {'data': crud.avg_by_level(db)}

@app.get('/api/metadata')
def metadata(db: Session = Depends(get_db)):
    return crud.get_metadata(db)

@app.get('/api/jobs/export')
def export_jobs(db: Session = Depends(get_db)):
    """Export all jobs as CSV for download."""
    from fastapi.responses import StreamingResponse
    import io, csv

    rows = db.query(models.Job).all()
    si = io.StringIO()
    writer = csv.writer(si)
    headers = ['id','title','company','level','salary_raw','avg_salary_mil_vnd','location','skills','source','url','crawled_at']
    writer.writerow(headers)
    for r in rows:
        writer.writerow([
            r.id,
            r.title or '',
            r.company or '',
            r.level or '',
            r.salary_raw or '',
            r.avg_salary_mil_vnd if r.avg_salary_mil_vnd is not None else '',
            r.location or '',
            (r.skills or '').replace('\n', ' '),
            r.source or '',
            r.url or '',
            r.crawled_at or ''
        ])
    si.seek(0)
    return StreamingResponse(io.StringIO(si.getvalue()), media_type='text/csv', headers={'Content-Disposition': 'attachment; filename="jobs_export.csv"'})
# Admin: trigger import / crawl. For demo, trigger import of processed CSV files
from fastapi import Security
from .auth import get_current_admin_user
import subprocess
import threading
import time
import logging

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'admin_actions.log')

logger = logging.getLogger('admin')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(fh)

@app.post('/api/admin/import')
def admin_import(background_tasks: BackgroundTasks, admin_user = Security(get_current_admin_user)):
    from . import import_data
    background_tasks.add_task(import_data.import_processed_csvs)
    logger.info(f"User {admin_user.username} scheduled import")
    return {'status': 'import scheduled'}

@app.post('/api/admin/crawl')
def admin_crawl(background_tasks: BackgroundTasks, admin_user = Security(get_current_admin_user)):
    """Trigger crawling + process + import in background"""
    def job():
        logger.info(f"User {admin_user.username} started crawl")
        try:
            # run crawler script (file path)
            subprocess.run(['python', os.path.join('src','crawler','topcv_crawler.py')], check=False)
            # run processing script
            subprocess.run(['python', os.path.join('src','processing','salary_parser.py')], check=False)
            # import into DB
            from . import import_data
            import_data.import_processed_csvs()
            logger.info('Crawl/import finished')
        except Exception as e:
            logger.exception('Error during crawl')
    background_tasks.add_task(job)
    return {'status': 'crawl scheduled'}

from fastapi import Body
def admin_toggle_crawl(payload: dict = Body(...), admin_user = Security(get_current_admin_user)):
    enabled = int(payload.get('enabled', 1))
    db = SessionLocal()
    try:
        settings = db.query(models.AdminSetting).first()
        if not settings:
            settings = models.AdminSetting(crawl_enabled=1)
            db.add(settings)
        settings.crawl_enabled = 1 if enabled else 0
        db.commit()
        logger.info(f"User {admin_user.username} set crawl_enabled={settings.crawl_enabled}")
        return {'crawl_enabled': settings.crawl_enabled}
    finally:
        db.close()

@app.get('/api/admin/logs')
def admin_logs(lines: int = 200, admin_user = Security(get_current_admin_user)):
    if not os.path.exists(LOG_FILE):
        return {'logs': []}
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    return {'logs': data[-lines:]}

@app.get('/api/admin/settings')
def admin_settings(admin_user = Security(get_current_admin_user)):
    db = SessionLocal()
    try:
        s = db.query(models.AdminSetting).first()
        if not s:
            return {'crawl_enabled': 1}
        return {'crawl_enabled': s.crawl_enabled}
    finally:
        db.close()

from fastapi.security import OAuth2PasswordRequestForm
from .auth import verify_password, create_access_token

@app.post('/api/auth/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == form_data.username).first()
        if not user:
            raise HTTPException(status_code=400, detail='Incorrect username or password')
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail='Incorrect username or password')
        token = create_access_token({'sub': user.username})
        return {'access_token': token, 'token_type': 'bearer', 'role': user.role}
    finally:
        db.close()
# Salary Parsing utility endpoint
@app.post('/api/parse_salary')
def parse_salary_endpoint(payload: dict = Body(...)):
    """Parse a raw salary string and return normalized avg_salary_mil_vnd."""
    salary_str = payload.get('salary_raw', '')
    if not salary_str:
        return {'salary_raw': salary_str, 'avg_salary_mil_vnd': None, 'error': 'Empty salary string'}
    
    try:
        # Import parsing function
        import sys
        import os as os_module
        sys.path.insert(0, os_module.path.dirname(os_module.path.dirname(__file__)))
        from src.processing.salary_parser import parse_salary, USD_TO_VND_RATE
        
        min_sal, max_sal, currency = parse_salary(salary_str)
        
        # Calculate average
        avg_salary_mil_vnd = None
        if min_sal is not None and max_sal is not None:
            avg_sal = (min_sal + max_sal) / 2
        elif min_sal is not None:
            avg_sal = min_sal
        elif max_sal is not None:
            avg_sal = max_sal
        else:
            avg_sal = None
        
        # Convert USD to VND if needed
        if avg_sal is not None:
            if currency == 'USD':
                # USD values are typically monthly/annually, convert to millions VND
                avg_salary_mil_vnd = round(avg_sal * USD_TO_VND_RATE / 1_000_000, 2)
            else:
                # Assume already in millions VND
                avg_salary_mil_vnd = round(float(avg_sal), 2)
        
        return {
            'salary_raw': salary_str,
            'parsed': {'min': min_sal, 'max': max_sal, 'currency': currency},
            'avg_salary_mil_vnd': avg_salary_mil_vnd,
            'error': None
        }
    except Exception as e:
        logger.exception('Error parsing salary')
        return {
            'salary_raw': salary_str,
            'avg_salary_mil_vnd': None,
            'error': str(e)
        }

# Job Management endpoints (admin-only)
@app.post('/api/admin/jobs/create')
def admin_create_job(payload: dict = Body(...), admin_user = Security(get_current_admin_user)):
    """Create a new job (admin-only)."""
    db = SessionLocal()
    try:
        job = models.Job(
            title=payload.get('title'),
            company=payload.get('company'),
            level=payload.get('level'),
            salary_raw=payload.get('salary_raw'),
            avg_salary_mil_vnd=payload.get('avg_salary_mil_vnd'),
            location=payload.get('location'),
            skills=payload.get('skills', ''),
            source='manual',
            url=payload.get('url', ''),
            crawled_at=str(datetime.datetime.now())
        )
        db.add(job)
        db.commit()
        logger.info(f"User {admin_user.username} created job: {job.title}")
        return {'id': job.id, 'status': 'created'}
    except Exception as e:
        db.rollback()
        logger.exception('Error creating job')
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# ============ ADVANCED ANALYTICS ENDPOINTS ============

@app.get('/api/analytics/salary-stats')
def get_salary_stats(db: Session = Depends(get_db)):
    """Get comprehensive salary statistics"""
    jobs = db.query(models.Job).filter(models.Job.avg_salary_mil_vnd.isnot(None)).all()
    if not jobs:
        return {'count': 0}
    
    salaries = [j.avg_salary_mil_vnd for j in jobs]
    return {
        'count': len(salaries),
        'min': min(salaries),
        'max': max(salaries),
        'avg': sum(salaries) / len(salaries),
        'median': sorted(salaries)[len(salaries)//2]
    }

@app.get('/api/analytics/salary-by-level')
def get_salary_by_level(db: Session = Depends(get_db)):
    """Salary statistics by job level"""
    from sqlalchemy import func
    result = db.query(
        models.Job.level,
        func.count(models.Job.id).label('count'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary'),
        func.min(models.Job.avg_salary_mil_vnd).label('min_salary'),
        func.max(models.Job.avg_salary_mil_vnd).label('max_salary')
    ).filter(models.Job.avg_salary_mil_vnd.isnot(None)).group_by(models.Job.level).all()
    
    return [{
        'level': r[0] or 'Unknown',
        'count': r[1],
        'avg_salary': round(r[2], 2) if r[2] else 0,
        'min_salary': r[3],
        'max_salary': r[4]
    } for r in result]

@app.get('/api/analytics/salary-by-location')
def get_salary_by_location(limit: int = 15, db: Session = Depends(get_db)):
    """Top locations by average salary"""
    from sqlalchemy import func
    result = db.query(
        models.Job.location,
        func.count(models.Job.id).label('count'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary')
    ).filter(models.Job.avg_salary_mil_vnd.isnot(None)).group_by(models.Job.location).order_by(func.avg(models.Job.avg_salary_mil_vnd).desc()).limit(limit).all()
    
    return [{
        'location': r[0] or 'Unknown',
        'count': r[1],
        'avg_salary': round(r[2], 2) if r[2] else 0
    } for r in result]

@app.get('/api/analytics/top-skills')
def get_top_skills(limit: int = 20, db: Session = Depends(get_db)):
    """Extract and rank top skills by frequency and average salary"""
    from sqlalchemy import func
    jobs = db.query(models.Job).filter(models.Job.skills.isnot(None)).all()
    
    skill_map = {}
    for job in jobs:
        if job.skills:
            skills = [s.strip() for s in job.skills.split(',')]
            for skill in skills:
                if skill:
                    if skill not in skill_map:
                        skill_map[skill] = {'count': 0, 'total_salary': 0}
                    skill_map[skill]['count'] += 1
                    if job.avg_salary_mil_vnd:
                        skill_map[skill]['total_salary'] += job.avg_salary_mil_vnd
    
    result = [{
        'skill': k,
        'frequency': v['count'],
        'avg_salary': round(v['total_salary'] / v['count'], 2) if v['count'] > 0 else 0
    } for k, v in skill_map.items() if v['count'] >= 2]
    
    return sorted(result, key=lambda x: x['frequency'], reverse=True)[:limit]

@app.get('/api/analytics/salary-distribution')
def get_salary_distribution(bins: int = 10, db: Session = Depends(get_db)):
    """Salary distribution histogram data"""
    jobs = db.query(models.Job).filter(models.Job.avg_salary_mil_vnd.isnot(None)).all()
    if not jobs:
        return []
    
    salaries = [j.avg_salary_mil_vnd for j in jobs]
    min_sal = min(salaries)
    max_sal = max(salaries)
    bin_width = (max_sal - min_sal) / bins
    
    histogram = [{'bin': f'{min_sal + i*bin_width:.0f}-{min_sal + (i+1)*bin_width:.0f}', 'count': 0} for i in range(bins)]
    
    for salary in salaries:
        bin_idx = min(int((salary - min_sal) / bin_width), bins - 1)
        histogram[bin_idx]['count'] += 1
    
    return histogram

@app.get('/api/analytics/company-analysis')
def get_company_analysis(limit: int = 20, db: Session = Depends(get_db)):
    """Top companies by job count and average salary"""
    from sqlalchemy import func
    result = db.query(
        models.Job.company,
        func.count(models.Job.id).label('job_count'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary')
    ).filter(models.Job.avg_salary_mil_vnd.isnot(None)).group_by(models.Job.company).order_by(func.count(models.Job.id).desc()).limit(limit).all()
    
    return [{
        'company': r[0] or 'Unknown',
        'job_count': r[1],
        'avg_salary': round(r[2], 2) if r[2] else 0
    } for r in result]

@app.get('/api/analytics/title-salary-insights')
def get_title_salary_insights(limit: int = 15, db: Session = Depends(get_db)):
    """Job titles with highest average salary"""
    from sqlalchemy import func
    result = db.query(
        models.Job.title,
        func.count(models.Job.id).label('count'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary')
    ).filter(models.Job.avg_salary_mil_vnd.isnot(None)).group_by(models.Job.title).order_by(func.avg(models.Job.avg_salary_mil_vnd).desc()).limit(limit).all()
    
    return [{
        'title': r[0] or 'Unknown',
        'count': r[1],
        'avg_salary': round(r[2], 2) if r[2] else 0
    } for r in result]
@app.get('/api/analytics/data-sources')
def get_data_sources(db: Session = Depends(get_db)):
    """Get job count and stats by data source"""
    from sqlalchemy import func
    result = db.query(
        models.Job.source,
        func.count(models.Job.id).label('count'),
        func.min(models.Job.crawled_at).label('first_crawled'),
        func.max(models.Job.crawled_at).label('last_crawled'),
        func.avg(models.Job.avg_salary_mil_vnd).label('avg_salary')
    ).group_by(models.Job.source).all()
    
    return [{
        'source': r[0] or 'Unknown',
        'count': r[1],
        'first_crawled': r[2],
        'last_crawled': r[3],
        'avg_salary': round(r[4], 2) if r[4] else 0
    } for r in result]

@app.get('/api/analytics/trending-jobs')
def get_trending_jobs(days: int = 30, limit: int = 10, db: Session = Depends(get_db)):
    """Recently crawled jobs (last N days)"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    result = db.query(models.Job).filter(models.Job.crawled_at >= cutoff).order_by(models.Job.crawled_at.desc()).limit(limit).all()
    
    return [{
        'id': r.id,
        'title': r.title,
        'company': r.company,
        'salary': r.avg_salary_mil_vnd,
        'source': r.source,
        'crawled_at': r.crawled_at,
        'url': r.url
    } for r in result]

@app.get('/api/analytics/market-overview')
def get_market_overview(db: Session = Depends(get_db)):
    """Overall market insights"""
    from sqlalchemy import func
    total = db.query(func.count(models.Job.id)).scalar() or 0
    with_salary = db.query(func.count(models.Job.id)).filter(models.Job.avg_salary_mil_vnd.isnot(None)).scalar() or 0
    
    sources = db.query(
        models.Job.source,
        func.count(models.Job.id).label('count')
    ).group_by(models.Job.source).all()
    
    locations = db.query(
        models.Job.location,
        func.count(models.Job.id).label('count')
    ).group_by(models.Job.location).order_by(func.count(models.Job.id).desc()).limit(5).all()
    
    return {
        'total_jobs': total,
        'jobs_with_salary': with_salary,
        'data_completeness': round(with_salary / total * 100, 1) if total > 0 else 0,
        'sources': [{'name': s[0] or 'Unknown', 'count': s[1]} for s in sources],
        'top_locations': [{'location': l[0] or 'Unknown', 'count': l[1]} for l in locations]
    }

# ============ AUTOCOMPLETE/SUGGESTIONS ENDPOINTS ============

@app.get('/api/suggestions/titles')
def suggest_titles(q: str = '', limit: int = 10, db: Session = Depends(get_db)):
    """Get job title suggestions"""
    from sqlalchemy import func, distinct
    query = db.query(distinct(models.Job.title)).filter(models.Job.title.ilike(f'%{q}%')).limit(limit).all()
    return {'suggestions': [r[0] for r in query if r[0]]}

@app.get('/api/suggestions/companies')
def suggest_companies(q: str = '', limit: int = 10, db: Session = Depends(get_db)):
    """Get company name suggestions"""
    from sqlalchemy import func, distinct
    query = db.query(distinct(models.Job.company)).filter(models.Job.company.ilike(f'%{q}%')).limit(limit).all()
    return {'suggestions': [r[0] for r in query if r[0]]}

@app.get('/api/suggestions/locations')
def suggest_locations(q: str = '', limit: int = 10, db: Session = Depends(get_db)):
    """Get location suggestions"""
    from sqlalchemy import func, distinct
    query = db.query(distinct(models.Job.location)).filter(models.Job.location.ilike(f'%{q}%')).limit(limit).all()
    return {'suggestions': [r[0] for r in query if r[0]]}

@app.get('/api/suggestions/skills')
def suggest_skills(q: str = '', limit: int = 10, db: Session = Depends(get_db)):
    """Get skill suggestions"""
    jobs = db.query(models.Job).filter(models.Job.skills.ilike(f'%{q}%')).limit(50).all()
    
    skills_set = set()
    for job in jobs:
        if job.skills:
            for skill in job.skills.split(','):
                skill = skill.strip()
                if skill and skill.lower().startswith(q.lower()):
                    skills_set.add(skill)
    
    return {'suggestions': sorted(list(skills_set))[:limit]}

@app.get('/api/suggestions/levels')
def suggest_levels(q: str = '', db: Session = Depends(get_db)):
    """Get job level suggestions"""
    from sqlalchemy import func, distinct
    query = db.query(distinct(models.Job.level)).filter(models.Job.level.ilike(f'%{q}%')).all()
    return {'suggestions': [r[0] for r in query if r[0]]}

@app.get('/api/analytics/top-30-jobs')
def get_top_30_jobs(db: Session = Depends(get_db)):
    """Get top 30 highest paying jobs"""
    from sqlalchemy import func
    result = db.query(models.Job).filter(models.Job.avg_salary_mil_vnd.isnot(None)).order_by(models.Job.avg_salary_mil_vnd.desc()).limit(30).all()
    
    return [{
        'id': r.id,
        'title': r.title,
        'company': r.company,
        'level': r.level,
        'salary': round(r.avg_salary_mil_vnd, 1),
        'location': r.location,
        'skills': r.skills,
        'source': r.source,
        'url': r.url,
        'crawled_at': r.crawled_at
    } for r in result]