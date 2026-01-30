import os
import re
import glob
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template

# Set matplotlib backend to Agg to avoid GUI errors in a web server environment
matplotlib.use('Agg')

# Initialize Flask App
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- Data and Analysis Functions ---

def load_data():
    """
    Loads and parses the processed demo data.
    It robustly handles the salary column by parsing string values
    and provides a fallback mechanism for demo purposes.
    """
    # Try the demo-specific filename first, otherwise pick the latest processed CSV
    processed_dir = os.path.join('data', 'processed')
    candidate = os.path.join(processed_dir, 'processed_demo_data.csv')
    if os.path.exists(candidate):
        data_path = candidate
    else:
        # Pick the latest processed file if any
        files = glob.glob(os.path.join(processed_dir, '*.csv'))
        data_path = max(files, key=os.path.getctime) if files else None

    try:
        if not data_path:
            raise FileNotFoundError
        df = pd.read_csv(data_path, engine="python", on_bad_lines="skip")

        # --- Robust Salary Parsing ---
        # This function extracts numbers from strings like "30 triệu" or averages "30-50 triệu"
        def parse_salary(salary_str):
            if not isinstance(salary_str, str):
                return None
            
            numbers = [float(num) for num in re.findall(r'(\d+)', salary_str)]
            
            if not numbers:
                return None
            
            # If "USD" is in the string, convert to VND (approx. 25k)
            if 'usd' in salary_str.lower():
                # Assuming salary in USD is per month and in thousands, e.g., 2K USD -> 2 * 25
                return sum(numbers) / len(numbers) * 25 
            
            return sum(numbers) / len(numbers)

        if 'salary' in df.columns:
            df['avg_salary_mil_vnd'] = df['salary'].apply(parse_salary)
            df.dropna(subset=['avg_salary_mil_vnd'], inplace=True)
        else:
            # If 'salary' column doesn't even exist, create an empty column to avoid breaking next steps
            df['avg_salary_mil_vnd'] = None

    except FileNotFoundError:
        print(f"Warning: Data file not found at {data_path}. Using fallback data.")
        df = pd.DataFrame() # Create empty frame to trigger fallback

    # --- Fallback for Demo ---
    # If the dataframe is empty after loading/parsing, create a sample one.
    if df.empty:
        print("Warning: Dataframe is empty. Generating fallback demo data.")
        fallback_data = {
            'title': ['Senior Python Developer', 'Junior Data Analyst', 'DevOps Lead'],
            'company': ['TechCorp', 'Data Inc.', 'Cloud Solutions'],
            'location': ['Ho Chi Minh', 'Hanoi', 'Da Nang'],
            'salary': ['60 triệu', '20 triệu', '85 triệu'],
            'avg_salary_mil_vnd': [60, 20, 85]
        }
        df = pd.DataFrame(fallback_data)
        
    return df

def classify_level(title):
    """Classifies job title into experience levels."""
    # Ensure title is a string before calling .lower()
    title_str = str(title).lower()
    if any(keyword in title_str for keyword in ['intern', 'thực tập']):
        return 'Intern'
    if any(keyword in title_str for keyword in ['junior']):
        return 'Junior'
    if any(keyword in title_str for keyword in ['senior']):
        return 'Senior'
    if any(keyword in title_str for keyword in ['manager', 'trưởng phòng', 'leader', 'lead']):
        return 'Manager/Lead'
    if any(keyword in title_str for keyword in ['middle', 'mid-level']):
        return 'Middle'
    return 'Not Specified'

def generate_charts(df):
    """Generates and saves analysis charts."""
    if df.empty or 'avg_salary_mil_vnd' not in df.columns or df['avg_salary_mil_vnd'].isnull().all():
        # Added check for column existence and all-null values
        print("Error: Cannot generate charts due to empty or invalid data.")
        return None, None

    # Chart 1: Average Salary by Level
    # Use 'level' column if it exists, otherwise classify from 'title'
    if 'level' not in df.columns:
        df['level'] = df['title'].apply(classify_level)
        
    level_order = ['Intern', 'Junior', 'Middle', 'Senior', 'Manager/Lead']
    # Filter df to only include levels in our defined order
    filtered_df = df[df['level'].isin(level_order)]
    
    plt.figure(figsize=(8, 5))
    sns.barplot(data=filtered_df, x='level', y='avg_salary_mil_vnd', order=level_order, palette="viridis", ci=None) # ci=None removes error bars
    plt.title('Lương trung bình theo cấp bậc', fontsize=14)
    plt.xlabel('Cấp bậc')
    plt.ylabel('Lương trung bình (Triệu VND)')
    plt.tight_layout()
    chart1_filename = 'chart_by_level.png'
    plt.savefig(os.path.join(app.static_folder, chart1_filename))
    plt.close()

    # Chart 2: Top 5 Locations by Average Salary
    df['location_clean'] = df['location'].str.split(',').str[0].str.strip()
    salary_by_location = df.groupby('location_clean')['avg_salary_mil_vnd'].mean().sort_values(ascending=False).head(5)
    
    plt.figure(figsize=(8, 5))
    if not salary_by_location.empty:
        sns.barplot(x=salary_by_location.values, y=salary_by_location.index, palette="plasma")
        plt.title('Top 5 địa điểm lương cao nhất', fontsize=14)
        plt.xlabel('Lương trung bình (Triệu VND)')
        plt.ylabel('Địa điểm')
        plt.tight_layout()
    else:
        plt.text(0.5, 0.5, 'Không đủ dữ liệu về địa điểm', ha='center')

    chart2_filename = 'chart_by_location.png'
    plt.savefig(os.path.join(app.static_folder, chart2_filename))
    plt.close()
    
    return chart1_filename, chart2_filename

# --- Flask Routes ---

@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """Analysis page route."""
    df = load_data()
    
    # The error is now handled inside load_data, but as a double-check
    if df.empty:
        return render_template('analysis.html', error="Lỗi: Không thể tải hoặc xử lý dữ liệu. Vui lòng kiểm tra file data/processed/processed_demo_data.csv."), 500

    # Generate charts and get their filenames
    chart1_url, chart2_url = generate_charts(df.copy()) # Use copy to avoid modifying original df

    # --- Prepare data table for display ---
    # Gracefully handle missing columns for the display table
    display_cols = ['title', 'company', 'location', 'salary', 'avg_salary_mil_vnd']
    existing_cols = [col for col in display_cols if col in df.columns]
    
    df_display = df[existing_cols].copy()

    rename_map = {
        'title': 'Chức danh',
        'company': 'Công ty',
        'location': 'Địa điểm',
        'salary': 'Lương (raw)',
        'avg_salary_mil_vnd': 'Lương TB (triệu VND)'
    }
    df_display.rename(columns={k: v for k, v in rename_map.items() if k in df_display.columns}, inplace=True)

    # Format the salary column if it exists
    if 'Lương TB (triệu VND)' in df_display.columns:
        df_display['Lương TB (triệu VND)'] = df_display['Lương TB (triệu VND)'].map('{:,.1f}'.format)

    # Convert DataFrame to HTML, adding Bootstrap classes
    data_table_html = df_display.to_html(classes='table table-striped table-hover text-center', index=False, justify='center', na_rep='N/A')
    
    return render_template('analysis.html', 
                           data_table=data_table_html, 
                           chart1_url=chart1_url, 
                           chart2_url=chart2_url)


if __name__ == "__main__":
    os.makedirs(app.static_folder, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
