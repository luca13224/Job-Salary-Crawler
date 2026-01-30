from sqlalchemy.orm import Session
from . import models
from sqlalchemy import func
from typing import List, Optional, Tuple

def get_jobs(db: Session, skip: int = 0, limit: int = 100, title: Optional[str] = None, location: Optional[str] = None, level: Optional[str] = None, min_salary: Optional[float] = None, max_salary: Optional[float] = None, sort_by: Optional[str] = None, sort_dir: str = 'desc'):
    q = db.query(models.Job)
    if title:
        q = q.filter(models.Job.title.ilike(f"%{title}%"))
    if location:
        q = q.filter(models.Job.location.ilike(f"%{location}%"))
    if level:
        q = q.filter(models.Job.level.ilike(f"%{level}%"))
    if min_salary is not None:
        q = q.filter(models.Job.avg_salary_mil_vnd >= min_salary)
    if max_salary is not None:
        q = q.filter(models.Job.avg_salary_mil_vnd <= max_salary)

    # Sorting support
    sort_map = {
        'avg_salary': models.Job.avg_salary_mil_vnd,
        'title': models.Job.title,
        'company': models.Job.company,
        'location': models.Job.location,
        'level': models.Job.level,
        'id': models.Job.id
    }
    if sort_by in sort_map:
        col = sort_map[sort_by]
        if sort_dir == 'asc':
            q = q.order_by(col.asc())
        else:
            q = q.order_by(col.desc())
    else:
        # default
        q = q.order_by(models.Job.avg_salary_mil_vnd.desc())

    total = q.count()
    results = q.offset(skip).limit(limit).all()
    return results, total


def get_metadata(db: Session):
    """Return distinct locations and levels for filters."""
    locs = [r[0] for r in db.query(models.Job.location).filter(models.Job.location != None).distinct().all()]
    levels = [r[0] for r in db.query(models.Job.level).filter(models.Job.level != None).distinct().all()]
    # Clean and sort
    locs = sorted([l for l in locs if l and str(l).strip()])
    levels = sorted([l for l in levels if l and str(l).strip()])
    return {'locations': locs, 'levels': levels}

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

# Analytics

def salary_distribution(db: Session, max_val: Optional[float]=None):
    q = db.query(models.Job.avg_salary_mil_vnd).filter(models.Job.avg_salary_mil_vnd != None)
    if max_val:
        q = q.filter(models.Job.avg_salary_mil_vnd < max_val)
    vals = [r[0] for r in q.all()]
    return vals

def avg_by_location(db: Session, top_n: int = 10):
    q = db.query(models.Job.location, func.avg(models.Job.avg_salary_mil_vnd).label('avg'))\
        .filter(models.Job.avg_salary_mil_vnd.isnot(None))\
        .group_by(models.Job.location)\
        .order_by(func.avg(models.Job.avg_salary_mil_vnd).desc())\
        .limit(top_n)
    return [{'location': row[0], 'avg_salary': float(row[1]) if row[1] else 0} for row in q]

def avg_by_level(db: Session):
    q = db.query(models.Job.level, func.avg(models.Job.avg_salary_mil_vnd).label('avg'), func.count(models.Job.id).label('count'))\
        .filter(models.Job.avg_salary_mil_vnd.isnot(None))\
        .group_by(models.Job.level)\
        .order_by(func.avg(models.Job.avg_salary_mil_vnd).desc())
    return [{'level': row[0], 'avg_salary': float(row[1]) if row[1] else 0, 'count': int(row[2])} for row in q]
