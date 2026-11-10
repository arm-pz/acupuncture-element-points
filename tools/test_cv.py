import sys, os, pathlib
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ROOT = pathlib.Path(__file__).resolve().parent.parent
ART_DIR = pathlib.Path("C:/Users/abdul/.gemini/antigravity/brain/8aabb083-e170-4acf-84b2-0047221a9782/playwright-artifacts")
ART_DIR.mkdir(parents=True, exist_ok=True)

def test_cv():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"PageError: {exc}"))
        
        print("1. Visiting http://127.0.0.1:4174/cv ...")
        resp = page.goto("http://127.0.0.1:4174/cv", wait_until="networkidle")
        assert resp.status == 200, f"Expected status 200, got {resp.status}"
        
        # Verify title & kicker
        title = page.title()
        print(f"   Title: {title}")
        assert "Conception Vessel" in title
        
        # Verify 5 chips exist
        chips = page.locator(".pts .chip")
        count = chips.count()
        print(f"   Element chips count: {count}")
        assert count == 5, f"Expected 5 element chips, got {count}"
        
        # Take initial screenshot
        page.screenshot(path=str(ART_DIR / "cv_initial_desktop.png"), full_page=True)
        print("   Saved cv_initial_desktop.png")
        
        # Click on CV6 (Water)
        chip_cv6 = page.locator('.chip[data-id="p6"]')
        chip_cv6.click()
        page.wait_for_timeout(300)
        
        info_html = page.locator("#pt-info").inner_html()
        assert "CV6" in info_html
        assert "Qihai" in info_html
        assert "Water" in info_html
        assert "1.5 cun" in info_html
        print("   CV6 (Water) selection verified!")
        
        # Click on CV5 (Fire)
        chip_cv5 = page.locator('.chip[data-id="p5"]')
        chip_cv5.click()
        page.wait_for_timeout(300)
        info_html5 = page.locator("#pt-info").inner_html()
        assert "CV5" in info_html5
        assert "Shimen" in info_html5
        assert "Fire" in info_html5
        assert "2.5 cun" in info_html5
        print("   CV5 (Fire) selection verified!")

        # Click on CV13 (Earth)
        chip_cv13 = page.locator('.chip[data-id="p13"]')
        chip_cv13.click()
        page.wait_for_timeout(300)
        info_html13 = page.locator("#pt-info").inner_html()
        assert "CV13" in info_html13
        assert "Shangwan" in info_html13
        assert "Earth" in info_html13
        assert "5.0 cun" in info_html13
        print("   CV13 (Earth) selection verified!")

        # Click on CV9 (Metal/Air)
        chip_cv9 = page.locator('.chip[data-id="p9"]')
        chip_cv9.click()
        page.wait_for_timeout(300)
        info_html9 = page.locator("#pt-info").inner_html()
        assert "CV9" in info_html9
        assert "Shuifen" in info_html9
        assert "Metal" in info_html9
        assert "1.0 cun" in info_html9
        print("   CV9 (Metal/Air) selection verified!")

        # Click on CV7 (Wood)
        chip_cv7 = page.locator('.chip[data-id="p7"]')
        chip_cv7.click()
        page.wait_for_timeout(300)
        info_html7 = page.locator("#pt-info").inner_html()
        assert "CV7" in info_html7
        assert "Yinjiao" in info_html7
        assert "Wood" in info_html7
        assert "1.0 cun" in info_html7
        print("   CV7 (Wood) selection verified!")
        
        # Test mobile viewport
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=str(ART_DIR / "cv_mobile_view.png"), full_page=True)
        print("   Saved cv_mobile_view.png")
        
        # Test Channels page link to CV
        print("2. Visiting http://127.0.0.1:4174/channels ...")
        page.goto("http://127.0.0.1:4174/channels", wait_until="networkidle")
        cv_route = page.locator('.route[data-ch="CV"]')
        assert cv_route.count() == 1, "Conception Vessel route not found in channels.html"
        print("   CV route found in channels.html!")
        page.screenshot(path=str(ART_DIR / "channels_cv_section.png"), full_page=False)

        # Test Points page search for CV
        print("3. Visiting http://127.0.0.1:4174/points ...")
        page.goto("http://127.0.0.1:4174/points", wait_until="networkidle")
        page.fill("#q", "CV6")
        page.wait_for_timeout(300)
        points_list = page.locator("#list li")
        assert points_list.count() == 1
        assert "Qihai" in points_list.first.inner_text()
        print("   CV points searchable in points.html!")
        
        browser.close()

    if errors:
        print("Encountered errors:")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    else:
        print("ALL TESTS PASSED WITH 0 CONSOLE ERRORS!")

if __name__ == "__main__":
    test_cv()
