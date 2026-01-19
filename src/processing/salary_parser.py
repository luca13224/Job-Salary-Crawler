import pandas as pd
import numpy as np
import re
import os
import glob
from datetime import datetime

# For simplicity, using a fixed exchange rate.
USD_TO_VND_RATE = 25000 

def parse_salary(salary_str):
    """
    Parses a raw salary string into min, max, and currency.
    Returns a tuple (min_salary, max_salary, currency).
    Salary values are in millions for VND, and as is for USD.
    """
    if not isinstance(salary_str, str):
        return None, None, 'Negotiable'

    salary_str = salary_str.lower().strip()
    
    # Common case: "Thỏa thuận"
    if 'thỏa thuận' in salary_str or 'negotiable' in salary_str:
        return None, None, 'Negotiable'

    # --- Currency Detection ---
    currency = 'VND' # Default currency
    if 'usd' in salary_str or '$' in salary_str:
        currency = 'USD'
    
    # --- Clean numbers ---
    # Remove currency symbols and units for easier parsing
    salary_str = salary_str.replace('usd', '').replace('$', '').replace('vnd', '').strip()
    
    # --- Pattern Matching ---
    
    # Case 1: "Từ X triệu" or "Trên X triệu" or "From X" -> min_salary = X
    match = re.search(r'(?:từ|trên|from)\s*([\d,.]+)', salary_str)
    if match:
        min_val = float(match.group(1).replace(',', ''))
        return min_val, None, currency

    # Case 2: "Lên đến X triệu" or "Tối đa X triệu" or "Up to X" -> max_salary = X
    match = re.search(r'(?:lên đến|tối đa|up to)\s*([\d,.]+)', salary_str)
    if match:
        max_val = float(match.group(1).replace(',', ''))
        return None, max_val, currency

    # Case 3: "X - Y triệu" or "X - Y"
    match = re.search(r'([\d,.]+)\s*-\s*([\d,.]+)', salary_str)
    if match:
        min_val = float(match.group(1).replace(',', ''))
        max_val = float(match.group(2).replace(',', ''))
        return min_val, max_val, currency

    # Case 4: A single number "X triệu" or just "X"
    match = re.search(r'([\d,.]+)', salary_str)
    if match:
        val = float(match.group(1).replace(',', ''))
        # If the string contains "triệu" it could be a single value, treat it as a range midpoint
        # For simplicity, we'll assign it as both min and max for now.
        return val, val, currency
        
    return None, None, 'Unparsed'

def process_raw_data(input_path):
    """
    Loads raw data, parses salaries, and adds standardized salary columns.

    Args:
        input_path (str): Path to the raw CSV file.

    Returns:
        pd.DataFrame: A DataFrame with processed salary data.
    """
    print(f"Processing file: {input_path}")
    df = pd.read_csv(input_path)

    if 'salary' not in df.columns:
        print("Error: 'salary' column not found.")
        return pd.DataFrame()

    # Apply the parsing function
    parsed_salaries = df['salary'].apply(parse_salary)
    df[['min_salary_raw', 'max_salary_raw', 'currency']] = pd.DataFrame(parsed_salaries.tolist(), index=df.index)
    
    # --- Salary Standardization to VND (in millions) ---
    df['min_salary_mil_vnd'] = df['min_salary_raw']
    df['max_salary_mil_vnd'] = df['max_salary_raw']

    # Convert "triệu" and USD to millions of VND
    is_vnd = df['currency'] == 'VND'
    is_usd = df['currency'] == 'USD'
    
    # For USD, convert to millions of VND
    df.loc[is_usd, 'min_salary_mil_vnd'] = (df.loc[is_usd, 'min_salary_raw'] * USD_TO_VND_RATE) / 1_000_000
    df.loc[is_usd, 'max_salary_mil_vnd'] = (df.loc[is_usd, 'max_salary_raw'] * USD_TO_VND_RATE) / 1_000_000
    
    # --- Calculate Average Salary ---
    # For a single value (min=max), avg is that value.
    # For a range, avg is the mean.
    # If one is null, use the other.
    df['avg_salary_mil_vnd'] = df[['min_salary_mil_vnd', 'max_salary_mil_vnd']].mean(axis=1)
    
    # Fill avg salary where only one of min/max is available
    df['avg_salary_mil_vnd'].fillna(df['min_salary_mil_vnd'], inplace=True)
    df['avg_salary_mil_vnd'].fillna(df['max_salary_mil_vnd'], inplace=True)

    print(f"Processed {len(df)} records.")
    return df

def save_processed_data(df, original_filename):
    """
    Saves the processed DataFrame to the data/processed directory.
    """
    if df.empty:
        print("DataFrame is empty. No data to save.")
        return

    output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a new filename based on the original
    base_name = os.path.basename(original_filename)
    new_filename = f"processed_{base_name}"
    output_path = os.path.join(output_dir, new_filename)

    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Processed data saved successfully to {output_path}")

def get_latest_raw_file():
    """Finds the most recently created file in the data/raw directory."""
    raw_dir = os.path.join('data', 'raw')
    list_of_files = glob.glob(os.path.join(raw_dir, '*.csv'))
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == '__main__':
    print("Starting data processing...")
    
    latest_raw_file = get_latest_raw_file()
    
    if latest_raw_file:
        processed_df = process_raw_data(latest_raw_file)
        if not processed_df.empty:
            save_processed_data(processed_df, latest_raw_file)
    else:
        print("No raw data files found in data/raw. Please run the crawler first.")
        
    print("Processing finished.")
