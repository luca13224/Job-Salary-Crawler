import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import re

def get_latest_processed_file():
    """Finds the most recently created file in the data/processed directory."""
    processed_dir = os.path.join('data', 'processed')
    list_of_files = glob.glob(os.path.join(processed_dir, '*.csv'))
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def classify_level(title):
    """Classifies job title into experience levels based on keywords."""
    title = title.lower()
    if any(keyword in title for keyword in ['intern', 'thực tập']):
        return 'Intern'
    if any(keyword in title for keyword in ['junior']):
        return 'Junior'
    if any(keyword in title for keyword in ['senior']):
        return 'Senior'
    if any(keyword in title for keyword in ['manager', 'trưởng phòng', 'leader', 'lead']):
        return 'Manager/Lead'
    # Mid-level is often the default if no other keyword is present
    if any(keyword in title for keyword in ['middle', 'mid-level']):
        return 'Middle'
    return 'Not Specified'

def analyze_salary_distribution(df, output_dir):
    """Analyzes and plots the overall salary distribution."""
    print("\n--- 1. Phân tích phân bổ lương tổng thể ---")
    
    # Filter out extreme outliers for a more meaningful analysis (e.g., salaries > 150M VND)
    salary_data = df['avg_salary_mil_vnd'].dropna()
    salary_data = salary_data[salary_data < 150]

    if salary_data.empty:
        print("Không có đủ dữ liệu lương để phân tích.")
        return

    print(f"Lương trung bình (triệu VND): {salary_data.mean():.2f}")
    print(f"Lương trung vị (triệu VND): {salary_data.median():.2f}")
    print(f"Độ lệch chuẩn (triệu VND): {salary_data.std():.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.histplot(salary_data, bins=30, kde=True)
    plt.title('Phân bổ mức lương trung bình (Triệu VND)')
    plt.xlabel('Lương trung bình (Triệu VND)')
    plt.ylabel('Số lượng tin tuyển dụng')
    plt.grid(True)
    
    # Save plot
    plot_path = os.path.join(output_dir, 'salary_distribution.png')
    plt.savefig(plot_path)
    print(f"Biểu đồ phân bổ lương đã được lưu tại: {plot_path}")
    plt.close()

def analyze_by_location(df):
    """Analyzes average salary by location."""
    print("\n--- 2. Phân tích lương theo địa điểm ---")
    
    # Simple location cleaning
    df['location_clean'] = df['location'].str.split(',').str[0].str.strip()
    
    salary_by_location = df.groupby('location_clean')['avg_salary_mil_vnd'].mean().sort_values(ascending=False)
    
    print("10 địa điểm có mức lương trung bình cao nhất:")
    print(salary_by_location.head(10).round(2))

def analyze_by_level(df):
    """Analyzes average salary by classified experience level."""
    print("\n--- 3. Phân tích lương theo cấp bậc (ước tính) ---")
    df['level'] = df['title'].apply(classify_level)
    
    salary_by_level = df.groupby('level')['avg_salary_mil_vnd'].agg(['mean', 'count']).sort_values(by='mean', ascending=False)
    salary_by_level = salary_by_level[salary_by_level.index != 'Not Specified'] # Remove generic category

    print("Mức lương trung bình theo cấp bậc ước tính:")
    print(salary_by_level.round(2))

def main():
    """Main function to run the analysis."""
    print("Bắt đầu module phân tích dữ liệu...")

    latest_file = get_latest_processed_file()
    if not latest_file:
        print("Không tìm thấy file dữ liệu đã xử lý. Vui lòng chạy crawler và processor trước.")
        return

    print(f"Sử dụng file dữ liệu: {latest_file}")
    df = pd.read_csv(latest_file)

    # Ensure salary column is numeric
    df['avg_salary_mil_vnd'] = pd.to_numeric(df['avg_salary_mil_vnd'], errors='coerce')
    df.dropna(subset=['avg_salary_mil_vnd'], inplace=True)
    
    # Create output directory for charts
    output_chart_dir = os.path.join('results', 'charts')
    os.makedirs(output_chart_dir, exist_ok=True)

    # Run analyses
    analyze_salary_distribution(df, output_chart_dir)
    analyze_by_location(df)
    analyze_by_level(df)

    print("\nPhân tích hoàn tất.")

if __name__ == '__main__':
    main()
