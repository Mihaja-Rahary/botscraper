from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

# Configuration rapide
HEADLESS = False   # True si tu veux le navigateur invisible
MAX_POSTS = 3

def scrape_public_user(username):
    url = f"https://www.instagram.com/{username}/"
    posts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(url)
        time.sleep(5)  # attendre le chargement de la page

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Récupérer les liens de posts
        anchors = soup.find_all("a")
        seen = set()
        for a in anchors:
            href = a.get("href")
            if href and "/p/" in href and href not in seen:
                post_url = "https://www.instagram.com" + href
                posts.append(post_url)
                seen.add(href)
                if len(posts) >= MAX_POSTS:
                    break

        browser.close()
    return posts

if __name__ == "__main__":
    results = scrape_public_user("nasa")
    print(f"Posts trouvés pour @nasa : {len(results)}")
    for url in results:
        print(url)
