import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.api.routes import router

app = FastAPI(title="Saqib AI Portfolio Assistant")

# Update allow_origins with your real deployed frontend URL before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://saqib-khan.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serves frontend/ at the root so that visiting the URL opens the UI directly
app.mount("/", StaticFiles(directory=str(PROJECT_ROOT / "frontend"), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
