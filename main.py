import requests
from bs4 import BeautifulSoup
def get_bing_results(query, page_number):
    url = f"https://www.bing.com/search?q={query}&first={page_number}" # so bing is w
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            return links
    except requests.exceptions.ChunkedEncodingError as e:
        print("Error occurred during the request:", e)

    return []

def is_unblocked_game(url, allowed_domains):
    for domain in allowed_domains:
        if domain in url:
            return domain

    return None

def save_to_file(games, seen_links):
    if games:
        output_file = "outputs/games.txt" # Where the fun happens
        with open(output_file, "a") as file:
            for game in games:
                if game not in seen_links:
                    seen_links.add(game)
                    file.write(game + "\n")

if __name__ == "__main__":
    query = "unblocked games links pages.dev"
    allowed_domains = [".pages.dev"] # Last One Standing

    page_number = 0
    seen_links = set()  # To keep track of seen links

    while True: # OMG FOREVER LOOPS!!!
        links = get_bing_results(query, page_number)

        games = set()

        no_unblocked_games_found = True

        for link in links:
            href = link.get("href")
            if href and href.startswith("http"):
                domain = is_unblocked_game(href, allowed_domains)
                if domain:
                    no_unblocked_games_found = False
                    games.add(href)

        save_to_file(games, seen_links)

        if not no_unblocked_games_found:
            print(f"{len(games)} Found!")
            page_number += 1 # So this basically automatically goes to the next page to scrape, w feature.
        else:
            print("No Unblocked Games :(")
