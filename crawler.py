import requests

headers = {
    "User-Agent": "Mozilla/5.0 (OSINT Username Checker)"
}

SITES = {
    "Twitter": {
        "url": "https://twitter.com/{username}",
        "not_found_phrases": [
            "This account doesn’t exist",
            "Try searching for another"
        ]
    },
    "Instagram": {
        "url": "https://www.instagram.com/{username}/",
        "not_found_phrases": [
            "Sorry, this page isn't available"
        ]
    },
    "GitHub": {
        "url": "https://github.com/{username}",
        "not_found_phrases": [
            "Not Found"
        ]
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{username}",
        "not_found_phrases": [
            "This channel does not exist"
        ]
    }
}

def check_username(username: str):
    found = []

    for site, data in SITES.items():
        url = data["url"].format(username=username)
        try:
            r = requests.get(url, headers=headers, timeout=6)
            page_text = r.text.lower()

            if r.status_code == 200:
                if not any(p.lower() in page_text for p in data["not_found_phrases"]):
                    found.append({
                        "site": site,
                        "url": url
                    })
        except requests.exceptions.RequestException:
            pass

    return found
