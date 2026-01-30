
import csv
import random
import os

# Define the structure of the data
job_titles = [
    "Software Engineer", "Data Scientist", "DevOps Engineer", "QA Engineer", 
    "Project Manager", "Business Analyst", "Product Manager", "Data Analyst",
    "Frontend Developer", "Backend Developer", "Fullstack Developer", "Mobile Developer"
]
levels = {
    "Intern": (8, 12),
    "Junior": (10, 25),
    "Mid-level": (25, 45),
    "Senior": (40, 70),
    "Lead": (60, 90),
    "Manager": (70, 150)
}
locations = ["Ho Chi Minh", "Hanoi", "Da Nang", "Remote", "Others"]
skills = [
    "Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Azure", "GCP",
    "SQL", "NoSQL", "Docker", "Kubernetes", "Machine Learning", "Deep Learning"
]

# Generate the data
num_records = random.randint(300, 500)
data = []

for _ in range(num_records):
    level = random.choices(list(levels.keys()), weights=[5, 25, 35, 25, 5, 5], k=1)[0]
    min_salary, max_salary = levels[level]
    
    # Introduce some variability
    salary_range_width = (max_salary - min_salary) * 0.3
    salary = round(random.uniform(min_salary, max_salary) + random.uniform(-salary_range_width, salary_range_width))
    salary = max(5, salary) # Ensure salary is not unrealistically low
    
    # Make salary a nice round number
    if salary > 20:
        salary = int(round(salary / 5) * 5)
    
    record = {
        "job_title": random.choice(job_titles),
        "level": level,
        "salary": f"{salary} triệu", # Using "triệu" for VND millions
        "location": random.choices(locations, weights=[40, 40, 10, 5, 5], k=1)[0],
        "skills": ", ".join(random.sample(skills, k=random.randint(2, 5))),
        "source": "Sample data for demo purposes"
    }
    data.append(record)

# Write raw CSV (for processing pipeline)
raw_output_dir = os.path.join('data', 'raw')
os.makedirs(raw_output_dir, exist_ok=True)
raw_file_path = os.path.join(raw_output_dir, "topcv_demo_raw.csv")

# Use consistent column names expected by the processor/web app
fieldnames = ["title", "level", "salary", "location", "skills", "company", "source"]
# Add a placeholder company name if missing
for r in data:
    if 'company' not in r or not r.get('company'):
        r['company'] = 'Demo Company'
    # normalize job_title -> title
    r['title'] = r.pop('job_title') if 'job_title' in r else r.get('title', '')

with open(raw_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{k: r.get(k, '') for k in fieldnames} for r in data])

print(f"Successfully generated {num_records} raw records in {raw_file_path}")

# Convenience function for other scripts

def generate_sample_raw(num_records_override=None):
    """Generate a sample raw CSV for demo/testing."""
    global num_records, data
    if num_records_override:
        num = num_records_override
    else:
        num = num_records
    # Reuse existing generated data list
    os.makedirs(raw_output_dir, exist_ok=True)
    return raw_file_path

if __name__ == '__main__':
    generate_sample_raw()
