import requests
from bs4 import BeautifulSoup

def get_bing_results(query, num_pages=1):
    results = []
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
                    results.append(href)
    return results

def check_ultraviolet_proxies(proxies):
    verified_proxies = []
    for proxy in proxies:
        response = requests.get(proxy)
        if response.status_code == 200:
            page_content = response.text
            if "ultraviolet" in page_content.lower():
                verified_proxies.append(proxy)
    return verified_proxies

def save_to_file(proxies, output_file="outputs.txt"):
    with open(output_file, "w") as file:
        for proxy in proxies:
            file.write(proxy + "\n")

if __name__ == "__main__":
    query = "ultraviolet proxies"
    num_pages = 10  # You can adjust the number of pages to scrape
    results = get_bing_results(query, num_pages)
    verified_proxies = check_ultraviolet_proxies(results)

    if verified_proxies:
        save_to_file(verified_proxies)
        print(f"{len(verified_proxies)} ultraviolet proxies found and saved to outputs.txt.")
    else:
        print("No ultraviolet proxies found.")