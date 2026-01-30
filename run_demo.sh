#!/bin/bash
# Job Salary Analytics - Demo Runner for Linux/Mac

echo "========================================"
echo " Job Salary Dashboard - Demo Launcher"
echo "========================================"
echo ""

# Kill any existing processes on ports 8000 and 5173
echo "Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo "[1/2] Starting Backend (FastAPI on port 8000)..."
export PYTHONPATH=$(pwd)
python -m uvicorn backend.main:app --port 8000 --host 127.0.0.1 &
BACKEND_PID=$!

sleep 2

echo "[2/2] Starting Frontend (Vite on port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!

sleep 3

echo ""
echo "========================================"
echo "DEMO RUNNING!"
echo "========================================"
echo ""
echo "Backend:  http://127.0.0.1:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Login with: admin / demo123"
echo ""
echo "Opening dashboard in browser..."
sleep 1

# Try to open in default browser (works on Mac/Linux)
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait
