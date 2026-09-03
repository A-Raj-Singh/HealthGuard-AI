import html
import re
import requests
import xml.etree.ElementTree as ET

URL = "https://wsearch.nlm.nih.gov/ws/query"


def clean_html(text: str) -> str:
    """Remove HTML tags and decode HTML entities."""
    if not text:
        return ""

    # Remove HTML tags such as <span class="qt0">...</span>
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode HTML entities such as &amp; and &nbsp;
    text = html.unescape(text)

    # Clean up excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def search_medical_info(query: str, limit: int = 6):
    if not query.strip():
        return []

    try:
        response = requests.get(
            URL,
            params={
                "db": "healthTopics",
                "term": query,
                "retmax": limit,
            },
            timeout=10,
        )

        response.raise_for_status()

        root = ET.fromstring(response.text)

        results = []

        for doc in root.findall(".//document")[:limit]:
            title = ""
            summary = ""
            url = doc.attrib.get("url", "")

            for content in doc.findall("content"):
                name = content.attrib.get("name")

                text = "".join(content.itertext()).strip()

                if name == "title":
                    title = clean_html(text)

                elif name in ("FullSummary", "snippet"):
                    summary = clean_html(text)

            if title or summary:
                results.append(
                    {
                        "title": title,
                        "summary": summary,
                        "url": url,
                    }
                )

        return results

    except (requests.RequestException, ET.ParseError):
        return []