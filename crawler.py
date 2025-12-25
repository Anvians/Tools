import sys
import requests

# Check if username is provided
if len(sys.argv) < 2:
    print("Usage: python tool.py <username>")
    sys.exit(1)

username = sys.argv[1]
headers = {
    "User-Agent": "Mozilla/5.0 (OSINT Username Checker)"
}

# Websites and their profile URL patterns
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

print(f"\n[+] Checking username: {username}\n")

found = []

for site, data in SITES.items():
    url = data["url"].format(username=username)

    try:
        r = requests.get(url, headers=headers, timeout=6)
        page_text = r.text.lower()

        if r.status_code == 200:
            if any(phrase.lower() in page_text for phrase in data["not_found_phrases"]):
                print(f"[-] {site}: Not Found")
            else:
                print(f"[FOUND] {site}: {url}")
                found.append(url)
        else:
            print(f"[-] {site}: Not Found")

    except requests.exceptions.RequestException:
        print(f"[!] {site}: Request Failed")

print("\n[+] Final Results:")
for profile in found:
    print(profile)