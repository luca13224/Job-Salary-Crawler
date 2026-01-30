"""Run a local demo: generate raw sample data, process it, run analyzer and optionally start the web app.
Usage:
    python run_demo.py        # generate/process/analyze
    python run_demo.py --serve    # generate/process/analyze and start Flask server
"""
import argparse
import time
import subprocess
import webbrowser
import os

from generate_data import generate_sample_raw
from src.processing import salary_parser
from src.analytics import basic_analyzer

RAW_DIR = os.path.join('data', 'raw')
PROCESSED_DIR = os.path.join('data', 'processed')


def main(serve=False):
    print('Generating raw sample data...')
    raw_path = generate_sample_raw()

    # Process raw file
    print('Processing raw data...')
    df = salary_parser.process_raw_data(raw_path)
    if df.empty:
        print('Đã xảy ra lỗi khi xử lý dữ liệu. Kiểm tra đầu vào.')
        return

    processed_filename = salary_parser.save_processed_data(df, os.path.basename(raw_path))

    # Import into SQLite DB for FastAPI backend
    try:
        from backend import import_data
        print('Importing processed CSVs into SQLite DB...')
        import_data.import_processed_csvs()
    except Exception as e:
        print('Warning: failed to import into DB:', e)

    # Run analyzer
    print('Chạy phần phân tích (basic_analyzer)...')
    basic_analyzer.main()

    if serve:
        print('Khởi động backend (FastAPI) và frontend (Vite) trong tiến trình con...')
        # Start FastAPI backend
        p1 = subprocess.Popen(['uvicorn', 'backend.main:app', '--reload', '--port', '8000'])
        # Start frontend
        p2 = subprocess.Popen(['npm', 'run', 'dev'], cwd='frontend')

        print('Đang mở trình duyệt vào http://127.0.0.1:5173 (chờ server khởi động)...')
        time.sleep(3)
        webbrowser.open('http://127.0.0.1:5173')
        print('Web app đang chạy. Ctrl+C để dừng.')
        try:
            p1.wait()
            p2.wait()
        except KeyboardInterrupt:
            print('Dừng các tiến trình...')
            p1.terminate()
            p2.terminate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true', help='Start the Flask demo web app after running the pipeline')
    args = parser.parse_args()
    main(serve=args.serve)
