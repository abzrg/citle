"""\
Get DOI

Via scraping crossref.org
"""


import re
import sys
import requests


def main() -> int:
    """Main function"""

    if len(sys.argv) != 2:
        sys.exit("No search query is provided")
    query: str = sys.argv[1].replace(" ", "+")

    query_url: str = f"https://search.crossref.org/?from_ui=yes&q={query}"
    # In this case I have to provide a User-agent as header to bypass ip ban
    query_source: str = get_source(query_url, {"User-Agent": "Mozilla/5.0"})

    # Capture groups:
    #   1. Title
    #   2. DOI
    query_entries = re.findall(
        r"<td class='item-data'>.*?<p class='lead'>(.*?)</p>.*?"
        r"<div class='item-links'>.*?<a.*?>.*?"
        r"<i class='icon-external-link'></i>(.*?)</a>.*?</div>.*?</td>",
        query_source,
        flags=re.DOTALL,
    )

    # If we couldn't find one article or an ip ban happend
    if not query_entries:
        sys.exit("Article not found")

    # Prompt user to choose one entry
    for index, entry in enumerate(query_entries):
        entry_title: str = entry[0].strip()
        # entry_doi: str = entry[1]
        print(f"[{index + 1}] {entry_title}")

    while True:
        try:
            # -1 because list is zero-indexed in python
            choice: int = int(input("Entry: ")) - 1
        except ValueError:
            pass
        else:
            if choice >= 0:
                print(f"DOI: {query_entries[choice][1].strip()}")
                break

    return 0


def get_source(url: str, headers: dict[str, str]) -> str:
    """Returns html text of a webpage"""
    return requests.get(url, headers=headers).text


if __name__ == "__main__":
    raise SystemExit(main())
