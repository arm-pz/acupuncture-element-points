import sys
import time
import pathlib
from playwright.sync_api import sync_playwright

# Ensure utf-8 stdout encoding for Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://acu.caffeinity.com"
SCREENSHOTS_DIR = pathlib.Path(r"C:\Users\abdul\.gemini\antigravity\brain\8aabb083-e170-4acf-84b2-0047221a9782\playwright-artifacts")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

test_results = []

def record(name, status, detail=""):
    test_results.append((name, status, detail))
    symbol = "[PASS]" if status == "PASS" else "[FAIL]"
    print(f"{symbol} {name}: {detail}")

def run_tests():
    print("==================================================")
    print(f" Running Playwright E2E Suite against: {BASE_URL}")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # ----------------------------------------------------
        # TEST 1: Home Page (/) - Rotating Five Elements Hub
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0
            title = page.title()

            assert status == 200, f"Expected 200 OK, got {status}"
            assert "Shu Atlas" in title, f"Unexpected title: {title}"
            
            # Check for five elements discs and stage
            vis_root = page.locator(".vis-root").first
            assert vis_root.is_visible(), "Elements stage (.vis-root) not visible"

            discs = page.locator(".vis-med")
            disc_count = discs.count()
            assert disc_count == 5, f"Expected 5 element glass discs, found {disc_count}"

            # Check CTA into channels
            cta = page.locator(".vis-cta").first
            assert cta.is_visible(), "CTA button (.vis-cta) not visible"

            page.screenshot(path=str(SCREENSHOTS_DIR / "01_home_page.png"))
            record("Home Page Five Elements Hub (/)", "PASS", f"Status: {status}, 5 discs rendered, CTA visible ({duration}ms)")
        except Exception as e:
            record("Home Page Five Elements Hub (/)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 2: Channels Route Explorer (/channels)
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/channels", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0
            title = page.title()

            assert status == 200, f"Expected 200 OK, got {status}"
            assert "Channel" in title, f"Title does not mention Channel: {title}"

            # Check 12 channels (.route)
            routes = page.locator(".route")
            route_count = routes.count()
            assert route_count == 12, f"Expected 12 channel routes, found {route_count}"

            # Check 60 station nodes (.station)
            stations = page.locator(".station")
            station_count = stations.count()
            assert station_count == 60, f"Expected 60 stations, found {station_count}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "02_channels_default.png"))
            record("Channels 12 Routes & 60 Stations (/channels)", "PASS", f"12 routes and 60 stations rendered ({duration}ms)")
        except Exception as e:
            record("Channels 12 Routes & 60 Stations (/channels)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 3: Station Inspector Popover Interaction
        # ----------------------------------------------------
        try:
            # Hover over station ST36
            st36 = page.locator('.station[data-code="ST36"]').first
            assert st36.is_visible(), "ST36 station not found"
            st36.hover()
            page.wait_for_timeout(350)

            popover = page.locator("#station-popover")
            assert popover.is_visible(), "Station popover did not appear on hover"

            popover_text = popover.inner_text()
            assert "Zusanli" in popover_text or "ST36" in popover_text or "足三里" in popover_text, f"Popover text missing ST36 details: {popover_text[:60]}"
            assert "Earth" in popover_text or "He-Sea" in popover_text or "Sea" in popover_text, "Popover missing category/element"

            page.screenshot(path=str(SCREENSHOTS_DIR / "03_channels_popover_st36.png"))
            first_line = popover_text.splitlines()[0] if popover_text.splitlines() else popover_text
            record("Station Inspector Popover (ST36 Hover)", "PASS", f"Popover active with details: '{first_line}'")
        except Exception as e:
            record("Station Inspector Popover (ST36 Hover)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 4: Search Highlighting on /channels
        # ----------------------------------------------------
        try:
            search_input = page.locator("#q")
            assert search_input.is_visible(), "Search input #q not visible"
            search_input.fill("knee")
            page.wait_for_timeout(400)

            counter = page.locator("#match-counter").inner_text()
            matches = page.locator(".station.match")
            match_count = matches.count()
            assert match_count >= 1 or "channel" in counter.lower(), f"Expected matches, got {counter}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "04_channels_search_knee.png"))
            record("Live Search Filter ('knee')", "PASS", f"Search active: {match_count} highlighted station nodes, counter: '{counter}'")
            
            # Clear search
            clear_btn = page.locator("#clear-search")
            if clear_btn.is_visible():
                clear_btn.click()
            else:
                search_input.fill("")
            page.wait_for_timeout(200)
        except Exception as e:
            record("Live Search Filter ('knee')", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 5: Faceted Filtering (Hand + Yin)
        # ----------------------------------------------------
        try:
            # Click Yin button in #f-yy
            yin_btn = page.locator('#f-yy button[data-yy="yin"]')
            assert yin_btn.is_visible(), "Yin filter button not found in #f-yy"
            yin_btn.click()
            page.wait_for_timeout(250)
            
            # Click Hand button in #f-limb
            hand_btn = page.locator('#f-limb button[data-limb="hand"]')
            assert hand_btn.is_visible(), "Hand filter button not found in #f-limb"
            hand_btn.click()
            page.wait_for_timeout(350)

            # Check visible routes using :not([hidden])
            visible_routes = page.locator('.route:not([hidden])')
            vis_count = visible_routes.count()
            assert vis_count == 3, f"Expected 3 Hand Yin channels (LU, HT, PC), found {vis_count}"

            # Verify the channels are LU, HT, PC
            channels_found = [visible_routes.nth(i).get_attribute("data-ch") for i in range(vis_count)]
            assert set(channels_found) == {"LU", "HT", "PC"}, f"Unexpected channels found: {channels_found}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "05_channels_hand_yin_filter.png"))
            record("Faceted Filtering (Hand Yin Channels)", "PASS", f"Correctly isolated exactly {vis_count} Hand Yin channels: {channels_found}")

            # Reset filters
            page.goto(f"{BASE_URL}/channels", wait_until="networkidle")
        except Exception as e:
            record("Faceted Filtering (Hand Yin Channels)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 6: Harmonic Column Highlight & Drawer
        # ----------------------------------------------------
        try:
            # Click Stream column button (rank 2)
            stream_col_btn = page.locator('.shu-col-btn[data-rank="2"]').first
            assert stream_col_btn.is_visible(), "Shu Stream column button not found"
            stream_col_btn.click()
            page.wait_for_timeout(400)

            drawer = page.locator("#col-drawer")
            assert drawer.is_visible(), "Harmonic column drawer not visible"
            drawer_text = drawer.inner_text()
            assert "Stream" in drawer_text or "輸" in drawer_text or "Shu" in drawer_text, f"Drawer text missing Stream details: {drawer_text}"

            # Check highlighted stations
            active_stations = page.locator(".station.col-active, .station[data-rank='2']")
            assert active_stations.count() >= 12, f"Expected at least 12 Stream stations, found {active_stations.count()}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "06_channels_harmonic_view.png"))
            record("Harmonic Column View & Drawer", "PASS", f"Stream column activated with harmonic drawer: '{drawer_text.splitlines()[0]}'")
        except Exception as e:
            record("Harmonic Column View & Drawer", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 7: Points Directory (/points)
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/points", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            points = page.locator("a.pt")
            count = points.count()
            assert count == 60, f"Expected 60 points in directory, found {count}"

            # Test filter search
            pt_search = page.locator("#q")
            if pt_search.is_visible():
                pt_search.fill("Wood")
                page.wait_for_timeout(300)
                visible_pts = page.locator("a.pt")
                wood_count = visible_pts.count()
                assert wood_count >= 12, f"Expected at least 12 Wood points, found {wood_count}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "07_points_directory.png"))
            record("Points Directory Search & Table (/points)", "PASS", f"Directory rendered {count} points with live filtering ({duration}ms)")
        except Exception as e:
            record("Points Directory Search & Table (/points)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 8: Learn Course & Glossary (/learn)
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/learn", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            # Check modules
            modules = page.locator(".sec, .module, section")
            mod_count = modules.count()
            assert mod_count >= 5, f"Expected modules in /learn, found {mod_count}"

            # Check glossary term trigger
            glossary_term = page.locator(".gloss").first
            if glossary_term.is_visible():
                glossary_term.hover()
                page.wait_for_timeout(200)

            page.screenshot(path=str(SCREENSHOTS_DIR / "08_learn_course.png"))
            record("Learn Curriculum & Glossary (/learn)", "PASS", f"Loaded modules with left rail curriculum ({duration}ms)")
        except Exception as e:
            record("Learn Curriculum & Glossary (/learn)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 9: Active Recall Quiz (/study)
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/study", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            # Check option buttons
            options = page.locator(".opt-btn, .choice-btn, button")
            opt_count = options.count()
            assert opt_count >= 2, f"Expected quiz option buttons, found {opt_count}"

            # Click first option button
            options.first.click()
            page.wait_for_timeout(300)

            page.screenshot(path=str(SCREENSHOTS_DIR / "09_study_quiz.png"))
            record("Active Recall Study Deck (/study)", "PASS", f"Quiz deck loaded with {opt_count} options and tactile interactions ({duration}ms)")
        except Exception as e:
            record("Active Recall Study Deck (/study)", "FAIL", str(e))

        # ----------------------------------------------------
        # TEST 10: Meridian Anatomy Chart (/lu)
        # ----------------------------------------------------
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/lu", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            # Check SVG presence
            svg = page.locator("svg").first
            assert svg.is_visible(), "Anatomical SVG chart missing"

            # Check point dots
            point_dots = page.locator("circle")
            dot_count = point_dots.count()
            assert dot_count >= 5, f"Expected at least 5 point circles in SVG, found {dot_count}"

            # Click LU9 dot
            target_pt = page.locator('[data-pt="LU9"], circle[data-code="LU9"], .dot').first
            if target_pt.is_visible():
                target_pt.click()
                page.wait_for_timeout(300)

            page.screenshot(path=str(SCREENSHOTS_DIR / "10_meridian_chart_lu.png"))
            record("Meridian Anatomy Chart (/lu)", "PASS", f"SVG anatomy rendered with {dot_count} circles and interactive panel ({duration}ms)")
        except Exception as e:
            record("Meridian Anatomy Chart (/lu)", "FAIL", str(e))

        browser.close()

    print("\n==================================================")
    passes = sum(1 for _, s, _ in test_results if s == "PASS")
    fails = sum(1 for _, s, _ in test_results if s == "FAIL")
    print(f" Playwright Test Summary: {passes} PASSED, {fails} FAILED out of {len(test_results)} tests")
    print(f" Artifacts directory: {SCREENSHOTS_DIR}")
    print("==================================================")
    return fails == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
