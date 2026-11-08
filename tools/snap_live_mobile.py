from playwright.sync_api import sync_playwright
import pathlib

out_dir = pathlib.Path(r"C:\Users\abdul\.gemini\antigravity\brain\8aabb083-e170-4acf-84b2-0047221a9782\playwright-artifacts")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto("https://acu.caffeinity.com/channels", wait_until="networkidle")

    # 1. Default Mobile View
    page.screenshot(path=str(out_dir / "mobile_live_01_default.png"))

    # 2. Type "knee" Search
    q = page.locator("#q")
    q.fill("knee")
    page.wait_for_timeout(350)
    page.screenshot(path=str(out_dir / "mobile_live_02_search_knee.png"))

    # 3. Clear Query
    q.fill("")
    page.wait_for_timeout(200)

    # 4. Multi-facet Filter: Hand + Yin
    page.locator('#f-yy button[data-yy="yin"]').click()
    page.locator('#f-limb button[data-limb="hand"]').click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(out_dir / "mobile_live_03_hand_yin.png"))

    # 5. Station Popover Tap
    st = page.locator('.station[data-code="LU9"]').first
    st.click()
    page.wait_for_timeout(350)
    page.screenshot(path=str(out_dir / "mobile_live_04_station_popover.png"))

    browser.close()
print("All live mobile captures completed successfully!")
