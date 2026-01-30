#!/usr/bin/env python
"""Quick import of processed CSVs into SQLite."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from backend.import_data import import_processed_csvs

if __name__ == '__main__':
    result = import_processed_csvs()
    print(f"\nImport complete: {result} jobs imported")
