
import json
import os
import urllib.request
import urllib.error
import html
import hashlib
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
    "TypeScript": "#3178C6",
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "Java": "#ED8B00",
    "Jupyter Notebook": "#F37626",
    "C": "#A8B9CC",
    "C++": "#00599C",
    "C#": "#9B4F96",
    "Shell": "#89E051",
    "PHP": "#777BB4",
    "Go": "#00ADD8",
    "Ruby": "#CC342D",
    "Kotlin": "#A97BFF",
    "Swift": "#F05138",
    "Dart": "#00B4AB",
    "Rust": "#DEA584",
    "SQL": "#E38C00",
}

def get_color(language):
    if language in COLORS:
        return COLORS[language]

    palette = [
        "#22D3EE", "#A78BFA", "#34D399",
        "#FB7185", "#FBBF24", "#60A5FA",
        "#C084FC", "#2DD4BF"
    ]

    index = int(
        hashlib.md5(language.encode()).hexdigest(), 16
    ) % len(palette)

    return palette[index]


def get_languages(repo):
    url = (
        f"https://api.github.com/repos/"
        f"{USERNAME}/{repo}/languages"
    )

    headers = {
        "User-Agent": "GitHub-Language-Dashboard",
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GH_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


totals = {}
errors = []

print("\nGITHUB LANGUAGE ANALYSIS")
print("=" * 45)

for repo in REPOS:
    try:
        languages = get_languages(repo)

        if not languages:
            print(f"\n{repo}: No detected languages")
            continue

        print(f"\n{repo}:")

        for language, size in languages.items():
            totals[language] = totals.get(language, 0) + size
            print(f"  {language}: {size:,} bytes")

    except Exception as error:
        errors.append(repo)
        print(f"\nERROR - {repo}: {error}")

# Never generate misleading partial statistics.
if errors:
    raise RuntimeError(
        "Some repositories could not be checked: "
        + ", ".join(errors)
    )

total_bytes = sum(totals.values())

if not total_bytes:
    raise RuntimeError("No language data found.")

languages = sorted(
    totals.items(),
    key=lambda item: item[1],
    reverse=True
)

# Dashboard dimensions
width = 1100
row_height = 76
top_space = 210
bottom_space = 75
height = top_space + len(languages) * row_height + bottom_space

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',

    """
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#020617"/>
        <stop offset="100%" stop-color="#0B1930"/>
      </linearGradient>

      <linearGradient id="border">
        <stop offset="0%" stop-color="#00E5FF"/>
        <stop offset="100%" stop-color="#2563EB"/>
      </linearGradient>

      <filter id="glow">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    """,

    f'<rect width="{width}" height="{height}" rx="28" fill="url(#bg)"/>',

    f'<rect x="4" y="4" width="{width-8}" '
    f'height="{height-8}" rx="25" '
    f'fill="none" stroke="url(#border)" stroke-width="4"/>',

    '<text x="55" y="78" fill="#FFFFFF" '
    'font-size="39" font-weight="bold">'
    'MOST USED PROGRAMMING LANGUAGES</text>',

    '<text x="55" y="125" fill="#22D3EE" '
    'font-size="22" font-weight="bold">'
    f'{len(languages)} LANGUAGES DETECTED'
    '</text>',

    '<text x="55" y="165" fill="#94A3B8" '
    'font-size="19">'
    f'Across {len(REPOS)} public GitHub repositories'
    '</text>',

    '<line x1="55" y1="185" x2="1045" y2="185" '
    'stroke="#1E3A5F" stroke-width="2"/>'
]

y = top_space

for language, size in languages:

    percentage = size / total_bytes * 100
    color = get_color(language)
    safe_language = html.escape(language)

    bar_width = 560 * percentage / 100

    svg.append(
        f'<text x="60" y="{y}" fill="#FFFFFF" '
        f'font-size="25" font-weight="bold">'
        f'{safe_language}</text>'
    )

    svg.append(
        f'<rect x="350" y="{y-25}" width="560" '
        f'height="25" rx="12" fill="#263445"/>'
    )

    svg.append(
        f'<rect x="350" y="{y-25}" width="{bar_width:.2f}" '
        f'height="25" rx="12" fill="{color}" '
        f'filter="url(#glow)"/>'
    )

    svg.append(
        f'<text x="1035" y="{y}" fill="#FFFFFF" '
        f'font-size="23" font-weight="bold" '
        f'text-anchor="end">'
        f'{percentage:.2f}%</text>'
    )

    y += row_height

# Footer
svg.append(
    f'<text x="550" y="{height-30}" '
    f'fill="#22D3EE" font-size="18" '
    f'text-anchor="middle">'
    'CODE • BUILD • INNOVATE • REPEAT'
    '</text>'
)

svg.append("</svg>")

output = Path("assets/most-used-languages.svg")
output.parent.mkdir(parents=True, exist_ok=True)

output.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("\n" + "=" * 45)
print("LANGUAGE PERCENTAGE SUMMARY")
print("=" * 45)

for language, size in languages:
    percentage = size / total_bytes * 100
    print(f"{language}: {percentage:.2f}%")

print(f"\nTotal languages: {len(languages)}")
print(f"Repositories checked: {len(REPOS)}")
print("Dashboard generated successfully!")
