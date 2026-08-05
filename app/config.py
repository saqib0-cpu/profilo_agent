import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda *args, **kwargs: None

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8000))

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not set. Set it in your .env file.")