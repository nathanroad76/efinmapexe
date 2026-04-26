"""
Quick local testing server with mock data.
No database required - uses mock router for frontend testing.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Use mock router instead of real one
from routers import market_mock as market

app = FastAPI(title="efinmap API (Mock Mode)", version="2.0.0-mock")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api/v1")

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 efinmap Mock Server starting...")
    print("=" * 50)
    print("\nAccess URLs:")
    print("  US Market:   http://localhost:8000/index.html")
    print("  HK Market:   http://localhost:8000/hk.html")
    print("  Asia Market: http://localhost:8000/asia.html")
    print("  Watchlist:   http://localhost:8000/watchlist.html")
    print("\nPress Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
