"""\
Get BibTeX ref

Via scraping google scholar
"""

import html
import re
import sys
import requests


def main() -> int:
    """Main Function"""

    if len(sys.argv) != 2:
        sys.exit("No search query is provided")
    query: str = sys.argv[1].replace(" ", "+")

    # Get html source of search page
    query_url: str = f"https://scholar.google.com/scholar?hl=en&q={query}&num=10&btnG="
    query_source: str = get_source(query_url, {})

    query_entries: list[tuple[str, str, str]] = get_query_entries(query_source)

    # Choose an article
    choice: int = get_choice(query_entries)

    # Get citation page for the chosen entry
    choice_id: str = query_entries[choice - 1][0]
    choice_source: str = get_source(
        f"http://scholar.google.com/scholar?q=info:{choice_id}:scholar.google.com/&output=cite",
        {},
    )

    if matches := re.search(r"href=\"(.*?scholar\.bib.*?)\"", choice_source):
        choice_url: str = html.unescape(matches.group(1))
        choice_ref: str = get_source(choice_url, {})
        print(choice_ref)

    return 0


def get_source(url: str, headers: dict[str, str]) -> str:
    """Returns html text of a webpage"""
    return requests.get(url, headers=headers).text


def get_query_entries(source: str) -> list[tuple[str, str, str]]:
    """Returns (id, url, title)"""
    matches: list[tuple[str, str, str]] = []
    if matches := re.findall(
        r"<h3 class=\"gs_rt\".*?>.*?id=\"(.*?)\" href=\"(.*?)\".*?>(.*?)</a></h3>",
        source,
    ):
        return matches
    return []


def get_choice(query_entries: list[tuple[str, str, str]]):
    """Show menu of entries and carefully get input from user"""
    for index, entry in enumerate(query_entries):
        # id: str = entry[0]
        query_url: str = entry[1]
        query_title: str = re.sub(r"</?b>", "", entry[2], flags=re.IGNORECASE)
        print(f"[{index + 1}]: {query_title} ({query_url})")
    while True:
        try:
            choice: int = int(input("Entry: "))
        except ValueError:
            pass
        else:
            if choice >= 0:
                return choice


if __name__ == "__main__":
    raise SystemExit(main())
