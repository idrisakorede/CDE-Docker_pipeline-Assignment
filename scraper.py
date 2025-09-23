import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "https://nr.soccerway.com"


async def load_all_matches(page):
    """Dismiss consent banner, then click 'Load previous' until all matches are visible."""

    # Handle cookie consent first
    try:
        consent_button = page.locator("button:has-text('Accept All')")
        if await consent_button.count() > 0 and await consent_button.is_visible():
            print("🍪 Accepting cookies...")
            await consent_button.click()
            await asyncio.sleep(1)
    except Exception:
        print("⚠️ No cookie banner found, continuing...")

    print("🔄 Expanding all matches by clicking 'Load previous'...")
    while True:
        button_span = page.locator("span:has-text('Load previous')")
        if await button_span.count() == 0:
            break

        try:
            print("➡️ Clicking 'Load previous'...")
            # Use JS to bypass overlay blocking
            button_handle = await button_span.element_handle()
            await page.evaluate("(el) => el.closest('button').click()", button_handle)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to click 'Load previous': {e}")
            break

    print("✅ All matches loaded.")



async def extract_match(match, index, total):
    """Extract data from a single match container with retry + verification."""
    for attempt in range(3):  # up to 3 retries
        try:
            # URL
            url = await match.locator("a[href*='/matches/']").get_attribute("href")

            # Teams
            teams = await match.locator("span.sc-1718759c-3").all()
            home_team = (await teams[0].inner_text()).strip() if len(teams) > 0 else None
            away_team = (await teams[1].inner_text()).strip() if len(teams) > 1 else None

            # Scores
            scores = await match.locator("span.jnsOHd.label.score").all()
            home_score = (await scores[0].inner_text()).strip() if len(scores) > 0 else None
            away_score = (await scores[1].inner_text()).strip() if len(scores) > 1 else None

            # Gameweek
            gameweek_locator = match.locator("xpath=preceding::span[contains(text(),'Game week')][1]")
            gameweek = await gameweek_locator.inner_text() if await gameweek_locator.count() > 0 else None
            if gameweek:
                gameweek = gameweek.replace("Game week", "").strip()

            # Date
            date_locator = match.locator("xpath=preceding::span[contains(@class,'jgDxUJ')][1]")
            date_text = await date_locator.inner_text() if await date_locator.count() > 0 else None

            # Verification
            if not home_team or not away_team or not url:
                raise ValueError("❌ Missing critical data (team or url)")

            match_data = {
                "gameweek": int(gameweek) if gameweek and gameweek.isdigit() else None,
                "date": date_text,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "url": f"{BASE_URL}{url}" if url else None
            }

            print(f"[{index}/{total}] ✅ Scraped: {home_team} vs {away_team} "
                  f"=> {home_score}-{away_score} (GW {gameweek}, {date_text})")
            return match_data

        except Exception as e:
            print(f"[{index}/{total}] ⚠️ Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(1)

    print(f"[{index}/{total}] ❌ Failed to scrape match after 3 attempts.")
    return None


async def scrape_season_matches(season_url: str, output_file: str = "results.json"):
    all_matches = []

    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🌍 Navigating to {season_url}")
        await page.goto(season_url, timeout=60000)

        # Expand all matches
        await load_all_matches(page)

        # Select all match containers
        matches = await page.locator("div.sc-f6b773a5-3").all()
        total = len(matches)
        print(f"🔎 Found {total} matches in DOM")

        # Process matches one by one
        for i, match in enumerate(matches, start=1):
            match_data = await extract_match(match, i, total)
            if match_data:
                all_matches.append(match_data)

        await browser.close()
        print("🛑 Browser closed.")

    # Save JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)

    print(f"✅ Scraped {len(all_matches)} valid matches and saved to {output_file}")


if __name__ == "__main__":
    season_url = "https://nr.soccerway.com/national/nigeria/premier-league/20242025/regular-season/r83939/matches/"
    asyncio.run(scrape_season_matches(season_url))
