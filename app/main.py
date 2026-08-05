from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Serves frontend/ at /static if you want FastAPI to host the widget too
app.mount("/static", StaticFiles(directory="frontend"), name="static")