import requests
from bs4 import BeautifulSoup

def get_bing_results(query, num_pages=1):
    results = set()
    for page in range(1, num_pages + 1):
        url = f"https://www.bing.com/search?q={query}&first={10 * (page - 1)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a")
                for link in links:
                    href = link.get("href")
                    if href and href.startswith("http"):
                        results.add(href)
        except requests.exceptions.ChunkedEncodingError as e:
            print("Error occurred during the request:", e)

    return results

def is_unblocked_game(url):
    allowed_domains = [".firebaseapp.com", ".pages.dev", ".web.app", ".vercel.app", ".github.io", ".netlify.app", ".repl.co", ".herokuapp.com", ".csb.app", ".cyclic.app"]
    matching_domains = []
    for domain in allowed_domains:
        if domain in url:
            matching_domains.append(domain)
    return matching_domains

def save_to_file(games, domain):
    output_file = f"{domain}.txt"
    with open(output_file, "w") as file:
        for game in games:
            file.write(game + "\n")


if __name__ == "__main__":
    query = "unblocked games links"
    num_pages = 100
    results = get_bing_results(query, num_pages)

    domain_files = {}
    for url in results:
        domains = is_unblocked_game(url)
        for domain in domains:
            if domain not in domain_files:
                domain_files[domain] = set()
            domain_files[domain].add(url)

    for domain, games in domain_files.items():
        save_to_file(games, domain)
        print(f"{len(games)} Found, I Put Em In {domain}!!")

    if not domain_files:
        print("No Unblocked Games :(")
