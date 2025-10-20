#!/bin/bash

# Stop all running servers

echo "Stopping Boardinghouse Management System..."

# Kill backend processes
pkill -f "python main.py"
pkill -f "uvicorn"

# Kill frontend processes
pkill -f "vite"
pkill -f "npm run dev"

echo "All servers stopped."
