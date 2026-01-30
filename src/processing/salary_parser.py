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
    Salary values are returned in 'triệu VND' (millions of VND) when currency is VND.
    USD values are converted to millions of VND when processed later.
    """
    if not isinstance(salary_str, str):
        return None, None, 'Negotiable'

    raw = salary_str.lower().strip()

    # Common case: "Thỏa thuận"
    if 'thỏa thuận' in raw or 'negotiable' in raw:
        return None, None, 'Negotiable'

    # --- Currency Detection ---
    currency = 'VND' # Default currency
    if 'usd' in raw or '$' in raw:
        currency = 'USD'

    # Detect unit words
    has_trieu = 'triệu' in raw
    has_k = re.search(r'\b(\d+\.?\d*)k\b', raw) is not None

    # Remove textual noise
    s = raw.replace('usd', '').replace('$', '').replace('vnd', '').replace('triệu', '').strip()

    # Pattern matching as before
    match = re.search(r'(?:từ|trên|from)\s*([\d,.]+)', s)
    if match:
        min_val = float(match.group(1).replace(',', ''))
        if has_trieu:
            return min_val, None, currency
        if has_k and currency == 'USD':
            return min_val, None, currency
        return min_val, None, currency

    match = re.search(r'(?:lên đến|tối đa|up to)\s*([\d,.]+)', s)
    if match:
        max_val = float(match.group(1).replace(',', ''))
        return None, max_val, currency

    match = re.search(r'([\d,.]+)\s*-\s*([\d,.]+)', s)
    if match:
        min_val = float(match.group(1).replace(',', ''))
        max_val = float(match.group(2).replace(',', ''))
        return min_val, max_val, currency

    match = re.search(r'([\d,.]+)k', raw)
    if match and currency == 'USD':
        # e.g., '2k USD' -> 2000 USD
        val = float(match.group(1).replace(',', '')) * 1000
        return val, val, currency

    match = re.search(r'([\d,.]+)', s)
    if match:
        val = float(match.group(1).replace(',', ''))
        # If original had 'triệu' we interpret value as millions of VND already
        if has_trieu:
            return val, val, currency
        # Otherwise return as-is (could be in units depending on currency)
        return val, val, currency

    return None, None, 'Unparsed'

# --- Normalize input columns in process_raw_data ---

def _normalize_columns(df):
    # Standardize title column
    if 'job_title' in df.columns and 'title' not in df.columns:
        df = df.rename(columns={'job_title': 'title'})
    # Ensure salary column exists
    if 'salary' not in df.columns and 'lương' in df.columns:
        df = df.rename(columns={'lương': 'salary'})
    return df

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

    df = _normalize_columns(df)

    if 'salary' not in df.columns:
        print("Error: 'salary' column not found.")
        return pd.DataFrame()

    # Apply the parsing function
    parsed_salaries = df['salary'].apply(parse_salary)
    df[['min_salary_raw', 'max_salary_raw', 'currency']] = pd.DataFrame(parsed_salaries.tolist(), index=df.index)
    
    # --- Salary Standardization to VND (in millions) ---
    df['min_salary_mil_vnd'] = df['min_salary_raw']
    df['max_salary_mil_vnd'] = df['max_salary_raw']

    # Convert USD to millions of VND when necessary
    is_usd = df['currency'] == 'USD'
    df.loc[is_usd, 'min_salary_mil_vnd'] = (df.loc[is_usd, 'min_salary_raw'] * USD_TO_VND_RATE) / 1_000_000
    df.loc[is_usd, 'max_salary_mil_vnd'] = (df.loc[is_usd, 'max_salary_raw'] * USD_TO_VND_RATE) / 1_000_000

    # Ensure numeric types
    df['min_salary_mil_vnd'] = pd.to_numeric(df['min_salary_mil_vnd'], errors='coerce')
    df['max_salary_mil_vnd'] = pd.to_numeric(df['max_salary_mil_vnd'], errors='coerce')

    # --- Calculate Average Salary ---
    df['avg_salary_mil_vnd'] = df[['min_salary_mil_vnd', 'max_salary_mil_vnd']].mean(axis=1)
    df['avg_salary_mil_vnd'].fillna(df['min_salary_mil_vnd'], inplace=True)
    df['avg_salary_mil_vnd'].fillna(df['max_salary_mil_vnd'], inplace=True)

    print(f"Processed {len(df)} records.")
    return df

# Calculate avg salary safely and avoid chained-assignment warnings
    df['avg_salary_mil_vnd'] = df[['min_salary_mil_vnd', 'max_salary_mil_vnd']].mean(axis=1)
    df['avg_salary_mil_vnd'] = df['avg_salary_mil_vnd'].fillna(df['min_salary_mil_vnd'])
    df['avg_salary_mil_vnd'] = df['avg_salary_mil_vnd'].fillna(df['max_salary_mil_vnd'])

    print(f"Processed {len(df)} records.")
    return df

def save_processed_data(df, original_filename):
    """
    Saves the processed DataFrame to the data/processed directory and returns the output path.
    """
    if df.empty:
        print("DataFrame is empty. No data to save.")
        return None

    output_dir = os.path.join('data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a new filename based on the original
    base_name = os.path.basename(original_filename)
    new_filename = f"processed_{base_name}"
    output_path = os.path.join(output_dir, new_filename)

    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Processed data saved successfully to {output_path}")
    return output_path

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
