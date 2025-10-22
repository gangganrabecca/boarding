from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Simple test app without complex startup logic
app = FastAPI(title="Boardinghouse Management System - Test")

@app.get("/")
async def root():
    return {"message": "Boardinghouse API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
