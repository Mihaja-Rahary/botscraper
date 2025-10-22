# insta_scraper.py
import asyncio
from playwright.async_api import async_playwright
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, HEADLESS, MAX_POSTS, SLEEP_AFTER_NAV

async def login_instagram(page):
    await page.goto("https://www.instagram.com/accounts/login/")
    await page.fill("input[name='username']", INSTAGRAM_USERNAME)
    await page.fill("input[name='password']", INSTAGRAM_PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(5000)

async def fetch_post(page, link, content_type="posts"):
    await page.goto(link)
    await page.wait_for_timeout(2000)

    caption = await page.eval_on_selector(
        "div.C4VMK > span",
        "el => el.innerText",
        strict=False
    )
    hashtags = [tag.strip("#") for tag in caption.split() if tag.startswith("#")] if caption else []

    if content_type == "reels":
        video_url = await page.eval_on_selector(
            "video",
            "el => el.src",
            strict=False
        )
        return {
            "url": link,
            "caption": caption or "",
            "hashtags": hashtags,
            "likes": 0,  # Instagram ne montre plus likes sur Reels facilement
            "video": video_url
        }
    else:
        image_url = await page.eval_on_selector(
            "article img",
            "el => el.src",
            strict=False
        )
        likes_text = await page.eval_on_selector(
            "section span",
            "el => el.innerText",
            strict=False
        )
        likes = int(likes_text.replace(",", "")) if likes_text and likes_text.isdigit() else 0
        return {
            "url": link,
            "caption": caption or "",
            "hashtags": hashtags,
            "likes": likes,
            "image": image_url
        }

async def scrape_instagram_user(username, content_type="posts"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()
        await login_instagram(page)
        if content_type == "reels":
            await page.goto(f"https://www.instagram.com/{username}/reels/")
        else:
            await page.goto(f"https://www.instagram.com/{username}/")
        await page.wait_for_timeout(SLEEP_AFTER_NAV * 1000)

        post_links = await page.eval_on_selector_all(
            "article a" if content_type == "posts" else "div a",
            "elements => elements.map(el => el.href).slice(0, {})".format(MAX_POSTS)
        )

        tasks = []
        for link in post_links:
            new_page = await browser.new_page()
            tasks.append(fetch_post(new_page, link, content_type=content_type))
        posts = await asyncio.gather(*tasks)
        await browser.close()
        return posts
