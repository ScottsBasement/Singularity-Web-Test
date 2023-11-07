import requests
from bs4 import BeautifulSoup

def get_bing_results(query, num_pages=1):
    results = set()
    for page in range(1, num_pages + 1):
        url = f"https://www.bing.com/search?q={query}&first={10 * (page - 1)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            for link in links:
                href = link.get("href")
                if href and href.startswith("http"):
                    results.add(href)
    return results

def is_unblocked_game(url):
    allowed_domains = [".github.io", ".firebaseapp.com", ".vercel.app", ".netlify.app", ".pages.dev"]
    for domain in allowed_domains:
        if domain in url:
            return domain  # Return the matched domain
    return None

def save_to_file(games, domain):
    output_file = f"{domain}.txt"  # Create a separate file for each domain
    with open(output_file, "w") as file:
        for game in games:
            file.write(game + "\n")

if __name__ == "__main__":
    query = "unblocked games"
    num_pages = 100
    results = get_bing_results(query, num_pages)

    domain_files = {}  # Create a dictionary to store links by domain
    for url in results:
        domain = is_unblocked_game(url)
        if domain:
            if domain not in domain_files:
                domain_files[domain] = set()
            domain_files[domain].add(url)

    for domain, games in domain_files.items():
        save_to_file(games, domain)
        print(f"{len(games)} Found, Sorted To {domain}!!")

    if not domain_files:
        print("No Unblocked Games :(")
