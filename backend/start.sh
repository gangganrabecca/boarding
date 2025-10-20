#!/bin/bash

# Boardinghouse Management System Startup Script

echo "Starting Boardinghouse Management System..."
echo "=========================================="

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Error: Backend virtual environment not found!"
    echo "Please run the installation first."
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "Error: Frontend dependencies not installed!"
    echo "Please run 'npm install' in the frontend directory."
    exit 1
fi

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "System started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
