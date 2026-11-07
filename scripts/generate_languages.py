
import json
import urllib.request
import urllib.error
from html import escape

USERNAME = "saaqibmohiddin"

REPOSITORIES = [
    "CineShield-AI",
    "Inventory-Management",
    "Smart-Hospital-Queue",
    "Banking-Management-System",
    "AI-Learning-Path-Generator",
    "Python-ChatBot",
    "Student-Management-System",
    "AI-Language-Translator",
]

OUTPUT_FILE = "assets/most-used-languages.svg"

COLORS = [
    "#2685FF",
    "#FF7043",
    "#F7DF1E",
    "#985EFF",
    "#00D9FF",
    "#35C9A5",
    "#E879F9",
    "#F59E0B",
    "#A3B8CC",
    "#EF4444",
]


def github_request(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHub-Language-Dashboard"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def collect_languages():
    totals = {}

    for repo in REPOSITORIES:
        url = (
            f"https://api.github.com/repos/"
            f"{USERNAME}/{repo}/languages"
        )

        try:
            languages = github_request(url)

            print(f"Checking: {repo}")

            for language, byte_count in languages.items():
                totals[language] = (
                    totals.get(language, 0) + byte_count
                )

        except urllib.error.HTTPError as error:
            print(f"Could not access {repo}: HTTP {error.code}")
            raise

        except Exception as error:
            print(f"Error checking {repo}: {error}")
            raise

    return totals


def create_svg(language_totals):
    total_bytes = sum(language_totals.values())

    if total_bytes == 0:
        raise ValueError("No language data found.")

    languages = sorted(
        language_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    width = 1000
    row_height = 67
    start_y = 205
    height = max(350, start_y + len(languages) * row_height + 85)

    parts = []

    parts.append(f'''
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}" height="{height}"
     viewBox="0 0 {width} {height}">

<defs>
  <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0B1930"/>
    <stop offset="100%" stop-color="#030712"/>
  </linearGradient>

  <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#00D9FF"/>
    <stop offset="100%" stop-color="#2563EB"/>
  </linearGradient>
</defs>

<rect width="1000" height="{height}" rx="24"
      fill="url(#background)"/>

<rect x="4" y="4" width="992" height="{height-8}" rx="21"
      fill="none" stroke="url(#border)" stroke-width="3"/>

<text x="500" y="65" text-anchor="middle"
      fill="#00D9FF" font-size="35"
      font-weight="bold" font-family="Arial">
  MOST USED LANGUAGES
</text>

<text x="500" y="105" text-anchor="middle"
      fill="#94A3B8" font-size="17" font-family="Arial">
  LANGUAGE DISTRIBUTION ACROSS 8 PUBLIC PROJECTS
</text>

<line x1="55" y1="130" x2="945" y2="130"
      stroke="#2563EB" stroke-width="2"/>

<text x="60" y="175" fill="#FFFFFF"
      font-size="17" font-family="Arial">
  LANGUAGE
</text>

<text x="940" y="175" text-anchor="end"
      fill="#FFFFFF" font-size="17" font-family="Arial">
  PERCENTAGE
</text>
''')

    for index, (language, byte_count) in enumerate(languages):
        percentage = byte_count / total_bytes * 100
        y = start_y + index * row_height
        color = COLORS[index % len(COLORS)]

        label = escape(language)
        percent_text = f"{percentage:.2f}%"

        bar_width = percentage / 100 * 540

        parts.append(f'''
<text x="60" y="{y}"
      fill="#FFFFFF" font-size="21"
      font-weight="bold" font-family="Arial">
  {label}
</text>

<rect x="275" y="{y-22}" width="540" height="19"
      rx="9" fill="#263445"/>

<rect x="275" y="{y-22}" width="{bar_width:.2f}" height="19"
      rx="9" fill="{color}"/>

<text x="940" y="{y-5}" text-anchor="end"
      fill="#FFFFFF" font-size="20"
      font-weight="bold" font-family="Arial">
  {percent_text}
</text>
''')

    parts.append(f'''
<line x1="55" y1="{height-55}" x2="945" y2="{height-55}"
      stroke="#2563EB" stroke-width="2"/>

<text x="500" y="{height-25}" text-anchor="middle"
      fill="#94A3B8" font-size="14" font-family="Arial">
  GITHUB LINGUIST • BYTE-WEIGHTED • {len(languages)} LANGUAGES
</text>

</svg>
''')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(parts))

    print("\nLanguage statistics generated successfully!")

    for language, byte_count in languages:
        percentage = byte_count / total_bytes * 100
        print(f"{language}: {percentage:.2f}%")

    print(f"\nSaved to: {OUTPUT_FILE}")


def main():
    print("GitHub Language Dashboard")
    print("=" * 35)

    language_data = collect_languages()
    create_svg(language_data)


if __name__ == "__main__":
    main()
