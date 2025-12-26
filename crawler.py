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
            r = requests.get(url, headers=headers, timeout=6, allow_redirects=True)
            # Normalize page text
            page_text = r.text.lower().replace("’", "'")  

            # Basic logic: if status 200 and not showing "not found" phrases
            if r.status_code == 200:
                # Some sites redirect invalid users, check final URL
                final_url = r.url.lower()
                expected_url = url.lower()
                not_found = any(p.lower() in page_text for p in data["not_found_phrases"])
                
                if not_found or final_url != expected_url:
                    print(f"[-] {site}: Not Found")
                else:
                    print(f"[FOUND] {site}: {url}")
                    found.append({
                        "site": site,
                        "url": url
                    })
            else:
                print(f"[-] {site}: Not Found")

        except requests.exceptions.RequestException as e:
            print(f"[!] {site}: Request Failed ({e})")

    return found
