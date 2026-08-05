CERTIFICATES = [
    # {"name": "DigiSkills 3.0 - DBI101 (Data & Business Intelligence)", "issuer": "DigiSkills", "year": "2025", "link": ""},
    # Add your real certificates here in the same format
]


def get_certificates_text() -> str:
    if not CERTIFICATES:
        return "No certificates added yet."
    lines = []
    for c in CERTIFICATES:
        lines.append(f"{c['name']} — {c['issuer']} ({c['year']})")
    return "\n".join(lines)