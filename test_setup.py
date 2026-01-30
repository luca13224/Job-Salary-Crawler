#!/usr/bin/env python
"""Test import and API endpoints."""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("STEP 1: Import processed CSVs into DB")
print("=" * 60)
from backend.import_data import import_processed_csvs
result = import_processed_csvs()
print(f"\n✓ Imported {result} jobs into SQLite\n")

print("=" * 60)
print("STEP 2: Check DB content")
print("=" * 60)
from backend.database import SessionLocal
from backend import models
db = SessionLocal()
try:
    count = db.query(models.Job).count()
    print(f"Total jobs in DB: {count}")
    if count > 0:
        print("\nSample jobs:")
        for j in db.query(models.Job).limit(3):
            print(f"  - {j.id}: {j.title[:40] if j.title else 'N/A'} | {j.company} | ${j.avg_salary_mil_vnd}M")
finally:
    db.close()

print("\n" + "=" * 60)
print("STEP 3: Test API endpoint (requires backend running on 8000)")
print("=" * 60)
import requests
time.sleep(1)
try:
    r = requests.get('http://127.0.0.1:8000/api/jobs', params={'page': 1, 'per_page': 5}, timeout=3)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Response: {len(data.get('items', []))} items, total: {data.get('total')}")
        if data.get('items'):
            for item in data['items'][:2]:
                print(f"  - {item.get('title', 'N/A')} @ {item.get('company')}")
    else:
        print(f"Error: {r.text[:200]}")
except requests.exceptions.ConnectionError:
    print("⚠ Backend not running on http://127.0.0.1:8000")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("✓ Test complete!")
print("=" * 60)
