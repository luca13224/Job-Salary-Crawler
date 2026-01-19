import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# Base URL for TopCV IT jobs search
BASE_URL = "https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026"

def get_job_details(job_url):
    """
    Fetches additional details from the job detail page.
    (This is a placeholder for future enhancement, e.g., to get job description)
    """
    try:
        response = requests.get(job_url)
        if response.status_code == 200:
            # Placeholder for detail parsing logic
            return "Detail page reached"
    except requests.RequestException:
        return "Could not fetch details"
    return None

def crawl_jobs(num_pages=1):
    """
    Crawls job listings from TopCV for a specified number of pages.

    Args:
        num_pages (int): The number of search result pages to crawl.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped job data.
    """
    all_jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, num_pages + 1):
        print(f"Crawling page {page}...")
        url = f"{BASE_URL}?page={page}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_postings = soup.find_all('div', class_='job-item-new-2023')

        if not job_postings:
            print(f"No job postings found on page {page}. The structure might have changed.")
            break

        for job in job_postings:
            try:
                title_tag = job.find('h3', class_='title')
                company_tag = job.find('a', class_='company-name-new-2023')
                salary_tag = job.find('span', class_='salary')
                location_tags = job.find_all('span', class_='address')

                title = title_tag.get_text(strip=True) if title_tag else None
                company = company_tag.get_text(strip=True) if company_tag else None
                job_url = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else None
                
                # Handle cases where salary is not disclosed
                salary = salary_tag.get_text(strip=True) if salary_tag else "Thỏa thuận"

                # Join multiple location parts if they exist
                locations = [loc.get_text(strip=True) for loc in location_tags]
                location = ", ".join(locations) if locations else None

                if title and company and job_url:
                    all_jobs.append({
                        'title': title,
                        'company': company,
                        'salary': salary,
                        'location': location,
                        'url': job_url,
                        'crawled_at': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error parsing a job item: {e}")
                continue # Move to the next job item

        # Respectful crawling: wait a bit between pages
        time.sleep(1) 

    if not all_jobs:
        print("Crawling finished, but no jobs were found. The website structure may have changed, or the search query returned no results.")
        return pd.DataFrame()

    return pd.DataFrame(all_jobs)

def save_data(df):
    """
    Saves the DataFrame to a CSV file in the data/raw directory.
    """
    if df.empty:
        print("DataFrame is empty. No data to save.")
        return

    # Ensure the target directory exists
    output_dir = os.path.join('data', 'raw')
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'topcv_jobs_{timestamp}.csv'
    output_path = os.path.join(output_dir, filename)

    # Save to CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Data saved successfully to {output_path}")

if __name__ == '__main__':
    print("Starting TopCV job crawler...")
    # For a demo, let's crawl the first 2 pages
    job_data = crawl_jobs(num_pages=2) 
    
    if not job_data.empty:
        save_data(job_data)
        print(f"Crawled {len(job_data)} jobs.")
    else:
        print("No jobs were crawled.")
    
    print("Crawler finished.")
