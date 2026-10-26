"""
Entry-point script to run the Smart Transaction Anomaly Detection & AML Platform.
Launches FastAPI backend and WebApp on http://localhost:8000
"""

import os
import sys
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

if __name__ == "__main__":
    banner = """
    ========================================================================
     [+] SMART TRANSACTION ANOMALY DETECTION & AML INTELLIGENCE PLATFORM [+]
    ========================================================================
     >> WebApp URL:     http://localhost:8000
     >> Swagger API:    http://localhost:8000/docs
     >> Default Admin:  admin  / Admin@123
     >> Default Analyst: analyst / Analyst@123
    ========================================================================
    """
    print(banner)
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=False)
