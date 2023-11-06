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

def is_valid_proxy(url):
    # Filter out URLs containing specific keywords like "github" and "docs"
    keywords_to_exclude = ["github", "docs", "npmjs"]
    for keyword in keywords_to_exclude:
        if keyword in url:
            return False
    return True

def find_ultraviolet_proxies(results):
    proxies = []
    for result in results:
        if "ultraviolet" in result.lower() and is_valid_proxy(result):
            proxies.append(result)
    return proxies

def save_to_file(proxies, output_file="outputs.txt"):
    with open(output_file, "w") as file:
        for proxy in proxies:
            file.write(proxy + "\n")

if __name__ == "__main__":
    query = "ultraviolet proxies"
    num_pages = 3  # You can adjust the number of pages to scrape
    results = get_bing_results(query, num_pages)
    ultraviolet_proxies = find_ultraviolet_proxies(results)

    if ultraviolet_proxies:
        save_to_file(ultraviolet_proxies)
        print(f"{len(ultraviolet_proxies)} valid ultraviolet proxies found and saved to outputs.txt.")
    else:
        print("No valid ultraviolet proxies found.")
