from pydantic import BaseModel
from typing import Optional

class JobOut(BaseModel):
    id: int
    title: Optional[str]
    company: Optional[str]
    level: Optional[str]
    salary_raw: Optional[str]
    avg_salary_mil_vnd: Optional[float]
    location: Optional[str]
    skills: Optional[str]
    source: Optional[str]
    url: Optional[str]
    crawled_at: Optional[str]

    class Config:
        from_attributes = True
