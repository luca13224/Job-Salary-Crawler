from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True)
    company = Column(String(256), index=True)
    level = Column(String(64), index=True)
    salary_raw = Column(String(128))
    avg_salary_mil_vnd = Column(Float, index=True)
    location = Column(String(256), index=True)
    skills = Column(Text)
    source = Column(String(128))
    url = Column(String(512))
    crawled_at = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(256))
    role = Column(String(64), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)


class AdminSetting(Base):
    __tablename__ = 'admin_settings'
    id = Column(Integer, primary_key=True, index=True)
    crawl_enabled = Column(Integer, default=1)  # 1 true, 0 false
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
