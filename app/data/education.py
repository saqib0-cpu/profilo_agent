EDUCATION = [
    {
        "degree": "BS Computer Science (AI/ML focus)",
        "institute": "NUML Islamabad",
        "years": "2022 - 2026",  # <-- update
        "highlights": [
            "Coursework: Machine Learning, Advanced Database Systems, Networking, "
            "Technical & Business Writing"
        ]
    },
]


def get_education_text() -> str:
    lines = []
    for e in EDUCATION:
        lines.append(f"{e['degree']} — {e['institute']} ({e['years']})")
        for h in e["highlights"]:
            lines.append(f"  - {h}")
    return "\n".join(lines)