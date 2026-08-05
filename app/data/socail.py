SOCIAL_LINKS = {
    "github": "https://github.com/saqib0-cpu",
    "linkedin": "https://www.linkedin.com/in/saqib-khan-a7445829b",   # <-- update
    "email": "saqibkhan15203@gmail.com",                     # <-- update
    "portfolio": "https://saqibkhanprofilo.vercel.app",
}


def get_social_text() -> str:
    return "\n".join(f"{k}: {v}" for k, v in SOCIAL_LINKS.items())