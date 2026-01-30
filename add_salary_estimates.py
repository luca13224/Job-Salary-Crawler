"""
Script để thêm salary data cho các jobs không có lương
Dựa trên job level và title để estimate salary hợp lý
"""
import sys
import os
import random
import re
sys.path.insert(0, 'backend')

from backend.database import SessionLocal
from backend import models

# Salary ranges theo level (triệu VND/tháng)
SALARY_RANGES = {
    'Intern': (3, 8),
    'Junior': (8, 18),
    'Mid-level': (18, 35),
    'Senior': (35, 60),
    'Lead': (50, 80),
    'Manager': (60, 100)
}

# Bonus multiplier cho một số keywords
KEYWORD_BONUS = {
    'blockchain': 1.3,
    'ai': 1.25,
    'machine learning': 1.25,
    'architect': 1.4,
    'tech lead': 1.3,
    'senior': 1.2,
    'lead': 1.3,
    'principal': 1.5,
    'director': 1.6,
    'head': 1.5
}

def estimate_salary(title, level):
    """Estimate salary dựa trên title và level"""
    if level not in SALARY_RANGES:
        level = 'Mid-level'
    
    min_sal, max_sal = SALARY_RANGES[level]
    
    # Apply keyword bonus
    title_lower = str(title).lower()
    multiplier = 1.0
    
    for keyword, bonus in KEYWORD_BONUS.items():
        if keyword in title_lower:
            multiplier = max(multiplier, bonus)
    
    # Add some randomness
    base = random.uniform(min_sal, max_sal)
    estimated = base * multiplier
    
    # Round to nearest 0.5 triệu
    estimated = round(estimated * 2) / 2
    
    return estimated

print("=" * 60)
print("💰 Adding Salary Data to Jobs")
print("=" * 60)

session = SessionLocal()

try:
    # Get jobs without salary
    jobs = session.query(models.Job).filter(
        models.Job.avg_salary_mil_vnd.is_(None)
    ).all()
    
    print(f"\n📊 Found {len(jobs)} jobs without salary data")
    print("🔧 Adding estimated salaries based on job level and title...\n")
    
    updated = 0
    for job in jobs:
        estimated_salary = estimate_salary(job.title, job.level)
        
        # Update job with estimated salary
        job.avg_salary_mil_vnd = estimated_salary
        job.salary_raw = f"~{estimated_salary} triệu (ước tính)"
        
        updated += 1
        if updated % 10 == 0:
            print(f"   Updated {updated} jobs...")
    
    session.commit()
    
    print(f"\n✅ Updated {updated} jobs with estimated salaries")
    
    # Verify
    total_jobs = session.query(models.Job).count()
    jobs_with_salary = session.query(models.Job).filter(
        models.Job.avg_salary_mil_vnd.isnot(None)
    ).count()
    
    completion_rate = (jobs_with_salary / total_jobs * 100) if total_jobs > 0 else 0
    
    print(f"\n📈 Database Stats:")
    print(f"   Total jobs: {total_jobs}")
    print(f"   Jobs with salary: {jobs_with_salary}")
    print(f"   Completion rate: {completion_rate:.1f}%")
    
    print("\n" + "=" * 60)
    print("✨ Done! Refresh your browser to see the data")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    session.rollback()
    raise
finally:
    session.close()
