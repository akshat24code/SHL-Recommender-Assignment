import json
from pydoc import html
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.shl.com"

CATALOG_URL = (
    "https://www.shl.com/"
    "solutions/products/product-catalog/"
)

OUTPUT_FILE = "catalog/catalog.json"


def fetch_requests():

    for attempt in range(3):

        try:

            response = requests.get(
                CATALOG_URL,
                timeout=30
            )

            response.raise_for_status()

            return response.text

        except Exception as e:

            print(f"Retry {attempt+1}: {e}")

            time.sleep(2 ** attempt)

    return None


def fetch_playwright():

    try:

        all_html = []

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            )

            for start in range(0, 240, 12):

                url = (
                    f"{CATALOG_URL}"
                    f"?start={start}&type=1"
                )

                print(f"Opening: {url}")

                page.goto(
                    url,
                    timeout=120000,
                    wait_until="networkidle"
                )

                page.wait_for_timeout(3000)

                html = page.content()

                all_html.append(html)

            browser.close()

            return "\n".join(all_html)

    except Exception as e:

        print(f"Playwright failed: {e}")

        return None

    except Exception as e:

        print(f"Playwright failed: {e}")

        return None

def infer_test_type(text: str):

    text = text.lower()

    mapping = {
        "ability": "A",
        "biodata": "B",
        "competency": "C",
        "development": "D",
        "knowledge": "K",
        "personality": "P",
        "skills": "S",
    }

    for key, value in mapping.items():

        if key in text:
            return value

    return "K"


def parse_catalog(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    assessments = []

    skipped = []

    cards = soup.select(
    "td.custom__table-heading__title a"
)

    for card in cards:

        href = card.get("href", "")

        if "/products/product-catalog/view/" not in href:
            continue

        full_url = urljoin(
            BASE_URL,
            href
        )

        name = card.get_text(strip=True)

        if len(name) < 3:
            continue

        if not name:

            skipped.append("missing_name")

            continue

        parent_text = (
            card.parent.get_text(
                " ",
                strip=True
            ).lower()
        )

        if "job solution" in parent_text:

            skipped.append(name)

            continue

        assessment = {
            "name": name,
            "url": full_url,
            "description": parent_text[:500],
            "test_type": infer_test_type(parent_text),
            "remote_testing": (
                "remote" in parent_text
            ),
            "adaptive": (
                "adaptive" in parent_text
            ),
            "duration_minutes": None,
        }

        assessments.append(assessment)

    unique = []

    seen = set()

    for item in assessments:

        if item["url"] not in seen:

            unique.append(item)

            seen.add(item["url"])

    return unique, skipped


def main():

    html = fetch_requests()

    if not html:

        print("Using Playwright fallback...")

        html = fetch_playwright()

    if not html:

        print("Failed to fetch catalog")

        return

    assessments, skipped = parse_catalog(html)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            assessments,
            f,
            indent=2
        )

    print(
        f"Scraped {len(assessments)} assessments"
    )

    print(
        f"Skipped {len(skipped)} items"
    )


if __name__ == "__main__":
    main()