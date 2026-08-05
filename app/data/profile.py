PROFILE = {
    "name": "Saqib",
    "title": "AI/ML Engineer & Full-Stack Developer",
    "location": "Pakistan",
    "summary": (
        "Final-year BS Computer Science (AI/ML focus) student. Builds agentic AI "
        "systems, full-stack web apps, and mobile apps. Comfortable across the "
        "whole AI stack — from LLM agent design to backend APIs to Flutter apps."
    ),
    "availability": "Open for freelance projects and internship opportunities.",
    "resume_url": "https://your-site.com/resume.pdf",  # <-- update this
}


def get_profile_text() -> str:
    p = PROFILE
    return (
        f"Name: {p['name']}\n"
        f"Title: {p['title']}\n"
        f"Location: {p['location']}\n"
        f"Summary: {p['summary']}\n"
        f"Availability: {p['availability']}"
    )