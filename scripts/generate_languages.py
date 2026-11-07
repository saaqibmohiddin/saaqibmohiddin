import json
import os
import urllib.request
from pathlib import Path

USERNAME = "saaqibmohiddin"

REPOS = [
    "CineShield-AI",
    "Inventory-Management",
    "Smart-Hospital-Queue",
    "Banking-Management-System",
    "AI-Learning-Path-Generator",
    "Python-ChatBot",
    "Student-Management-System",
    "AI-Language-Translator",
]

COLORS = {
    "Python": "#3776AB",
    "JavaScript": "#F7DF1E",
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "Java": "#ED8B00",
    "TypeScript": "#3178C6",
    "Jupyter Notebook": "#F37626",
    "C": "#A8B9CC",
    "C++": "#00599C",
    "Shell": "#89E051",
    "PHP": "#777BB4",
    "Go": "#00ADD8",
    "Ruby": "#CC342D",
}

def get_languages(repo):
    url = (
        f"https://api.github.com/repos/"
        f"{USERNAME}/{repo}/languages"
    )

    headers = {
        "User-Agent": "GitHub-Language-Dashboard"
    }

    token = os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url, headers=headers
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())

totals = {}

for repo in REPOS:
    try:
        languages = get_languages(repo)

        for language, size in languages.items():
            totals[language] = (
                totals.get(language, 0) + size
            )

        print(f"Updated: {repo}")

    except Exception as error:
        print(f"Error in {repo}: {error}")

total_bytes = sum(totals.values())

if not total_bytes:
    raise RuntimeError("No language data found.")

languages = sorted(
    totals.items(),
    key=lambda item: item[1],
    reverse=True
)

width = 1000
row_height = 72
height = 180 + len(languages) * row_height

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    """
    <defs>
      <linearGradient id="bg">
        <stop offset="0%" stop-color="#030712"/>
        <stop offset="100%" stop-color="#071827"/>
      </linearGradient>
      <linearGradient id="border">
        <stop offset="0%" stop-color="#00D9FF"/>
        <stop offset="100%" stop-color="#2563EB"/>
      </linearGradient>
    </defs>
    """,
    f'<rect width="100%" height="100%" rx="28" fill="url(#bg)"/>',
    f'<rect x="4" y="4" width="992" height="{height-8}" '
    f'rx="24" fill="none" stroke="url(#border)" stroke-width="4"/>',
    '<text x="50" y="75" fill="#00D9FF" '
    'font-size="38" font-weight="bold">'
    'MOST USED PROGRAMMING LANGUAGES</text>',
    '<text x="50" y="125" fill="#94A3B8" '
    'font-size="20">Across 8 public GitHub repositories</text>'
]

y = 195

for language, size in languages:
    percentage = size / total_bytes * 100
    color = COLORS.get(language, "#94A3B8")
    bar_width = percentage * 7.0

    svg.append(
        f'<text x="55" y="{y}" fill="#FFFFFF" '
        f'font-size="25" font-weight="bold">'
        f'{language}</text>'
    )

    svg.append(
        f'<rect x="300" y="{y-25}" width="550" '
        f'height="22" rx="11" fill="#263445"/>'
    )

    svg.append(
        f'<rect x="300" y="{y-25}" width="{bar_width:.2f}" '
        f'height="22" rx="11" fill="{color}"/>'
    )

    svg.append(
        f'<text x="930" y="{y}" fill="#FFFFFF" '
        f'font-size="23" text-anchor="end">'
        f'{percentage:.2f}%</text>'
    )

    y += row_height

svg.append("</svg>")

output = Path("assets/most-used-languages.svg")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(svg), encoding="utf-8")

print("Language dashboard generated successfully!")