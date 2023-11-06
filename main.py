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
    allowed_domains = [".github.io", ".vercel.app", ".netlify.app", ".pages.dev", ".firebaseapp.com"]
    for domain in allowed_domains:
        if domain in url:
            return True
    return False

def find_unblocked_games(results):
    unblocked_games = set()
    for result in results:
        if is_unblocked_game(result):
            unblocked_games.add(result)
    return unblocked_games

def save_to_file(games, output_file="outputs.txt"):
    with open(output_file, "w") as file:
        for game in games:
            file.write(game + "\n")

if __name__ == "__main__":
    query = "unblocked games"
    num_pages = 100
    results = get_bing_results(query, num_pages)
    unblocked_games = find_unblocked_games(results)

    if unblocked_games:
        save_to_file(unblocked_games)
        print(f"{len(unblocked_games)} Found!")
    else:
        print("No Unblocked Games :(")
