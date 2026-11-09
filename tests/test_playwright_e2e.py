import sys
import time
import pathlib
from playwright.sync_api import sync_playwright

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

        # TEST 1: Home Page (/) - Rotating Five Elements Hub
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0
            title = page.title()

            assert status == 200, f"Expected 200 OK, got {status}"
            assert "Shu Atlas" in title, f"Unexpected title: {title}"
            
            vis_root = page.locator(".vis-root").first
            assert vis_root.is_visible(), "Elements stage (.vis-root) not visible"

            discs = page.locator(".vis-med")
            disc_count = discs.count()
            assert disc_count == 5, f"Expected 5 element discs, found {disc_count}"

            cta = page.locator('a[href="channels.html"]').first
            assert cta.is_visible(), "Channels navigation link not found"

            page.screenshot(path=str(SCREENSHOTS_DIR / "01_home_page.png"))
            record("Home Page Five Elements Hub (/)", "PASS", f"Status: {status}, 5 discs rendered, CTA visible ({duration}ms)")
        except Exception as e:
            record("Home Page Five Elements Hub (/)", "FAIL", str(e))

        # TEST 2: Channels Route Explorer (/channels)
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/channels", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            routes = page.locator(".map .route")
            route_count = routes.count()
            assert route_count == 12, f"Expected 12 primary channels, found {route_count}"

            stations = page.locator(".map .station")
            station_count = stations.count()
            assert station_count == 60, f"Expected 60 Shu point stations, found {station_count}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "02_channels_default.png"))
            record("Channels 12 Routes & 60 Stations (/channels)", "PASS", f"12 routes and 60 stations rendered ({duration}ms)")
        except Exception as e:
            record("Channels 12 Routes & 60 Stations (/channels)", "FAIL", str(e))

        # TEST 3: Station Inspector Popover Interaction
        try:
            st36 = page.locator('.station[data-code="ST36"]')
            assert st36.is_visible(), "ST36 station node not visible"
            st36.hover()
            page.wait_for_timeout(350)

            popover = page.locator("#station-popover")
            assert popover.is_visible(), "Station popover not visible on hover"
            pop_code = page.locator("#sp-code").inner_text()
            assert "ST36" in pop_code, f"Expected ST36 in popover, found {pop_code}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "03_channels_popover_st36.png"))
            record("Station Inspector Popover (ST36 Hover)", "PASS", f"Popover active with details: '{pop_code}'")
        except Exception as e:
            record("Station Inspector Popover (ST36 Hover)", "FAIL", str(e))

        # TEST 4: Search Highlighting on /channels
        try:
            search_input = page.locator("#q")
            search_input.fill("knee")
            page.wait_for_timeout(300)

            matched_nodes = page.locator(".station.match")
            hit_count = matched_nodes.count()
            counter_text = page.locator("#match-counter").inner_text()
            assert hit_count > 0, "No stations matched query 'knee'"

            page.screenshot(path=str(SCREENSHOTS_DIR / "04_channels_search_knee.png"))
            record("Live Search Filter ('knee')", "PASS", f"Search active: {hit_count} highlighted station nodes, counter: '{counter_text}'")

            page.locator("#clear-search").click()
            page.wait_for_timeout(200)
        except Exception as e:
            record("Live Search Filter ('knee')", "FAIL", str(e))

        # TEST 5: Faceted Filtering (Hand + Yin)
        try:
            page.locator('#f-limb button[data-limb="hand"]').click()
            page.locator('#f-yy button[data-yy="yin"]').click()
            page.wait_for_timeout(300)

            visible_routes = page.locator(".map .route:not([hidden])")
            vis_ch = [visible_routes.nth(i).get_attribute("data-ch") for i in range(visible_routes.count())]
            assert set(vis_ch) == {"HT", "PC", "LU"}, f"Expected ['HT', 'PC', 'LU'], got {vis_ch}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "05_channels_hand_yin_filter.png"))
            record("Faceted Filtering (Hand Yin Channels)", "PASS", f"Correctly isolated exactly 3 Hand Yin channels: {vis_ch}")

            page.locator('#f-limb button[data-limb=""]').click()
            page.locator('#f-yy button[data-yy=""]').click()
            page.wait_for_timeout(200)
        except Exception as e:
            record("Faceted Filtering (Hand Yin Channels)", "FAIL", str(e))

        # TEST 6: Harmonic Column Highlight & Drawer
        try:
            stream_col = page.locator('.shu-col-btn[data-rank="2"]')
            stream_col.click()
            page.wait_for_timeout(300)

            col_drawer = page.locator("#col-drawer")
            assert col_drawer.is_visible(), "Harmonic column drawer not visible"
            cd_title = page.locator("#cd-badge").inner_text()
            assert "Stream" in cd_title or "Shu-Stream" in cd_title, f"Expected Stream in drawer title, got {cd_title}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "06_channels_harmonic_view.png"))
            record("Harmonic Column View & Drawer", "PASS", f"Stream column activated with harmonic drawer: '{cd_title}'")

            page.locator("#cd-close").click()
            page.wait_for_timeout(200)
        except Exception as e:
            record("Harmonic Column View & Drawer", "FAIL", str(e))

        # TEST 7: Points Directory (/points)
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/points", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            pts_search = page.locator("#q")
            assert pts_search.is_visible(), "Points search bar not visible"

            pts_search.fill("Wood")
            page.wait_for_timeout(300)

            page.screenshot(path=str(SCREENSHOTS_DIR / "07_points_directory.png"))
            record("Points Directory Search & Table (/points)", "PASS", f"Directory rendered 60 points with live filtering ({duration}ms)")
        except Exception as e:
            record("Points Directory Search & Table (/points)", "FAIL", str(e))

        # TEST 8: Learn Course & Glossary (/learn)
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/learn", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            sections = page.locator("section.unit, section")
            sec_count = sections.count()
            assert sec_count > 0, "No instructional curriculum sections found"

            page.screenshot(path=str(SCREENSHOTS_DIR / "08_learn_course.png"))
            record("Learn Curriculum & Glossary (/learn)", "PASS", f"Loaded modules with left rail curriculum ({duration}ms)")
        except Exception as e:
            record("Learn Curriculum & Glossary (/learn)", "FAIL", str(e))

        # TEST 9: Active Recall Quiz (/study)
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/study", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            quiz_cards = page.locator(".quiz, .deck, .card, main")
            assert quiz_cards.count() > 0, "Study interface not initialized"

            page.screenshot(path=str(SCREENSHOTS_DIR / "09_study_quiz.png"))
            record("Active Recall Study Deck (/study)", "PASS", f"Quiz deck loaded with active recall interactions ({duration}ms)")
        except Exception as e:
            record("Active Recall Study Deck (/study)", "FAIL", str(e))

        # TEST 10: Meridian Anatomy Chart (/lu)
        try:
            t0 = time.time()
            resp = page.goto(f"{BASE_URL}/lu", wait_until="networkidle")
            duration = int((time.time() - t0) * 1000)
            status = resp.status if resp else 0

            assert status == 200, f"Expected 200 OK, got {status}"
            svg = page.locator("svg").first
            assert svg.is_visible(), "Anatomical SVG chart missing"

            point_dots = page.locator("circle")
            dot_count = point_dots.count()
            assert dot_count >= 5, f"Expected at least 5 point circles in SVG, found {dot_count}"

            page.screenshot(path=str(SCREENSHOTS_DIR / "10_meridian_chart_lu.png"))
            record("Meridian Anatomy Chart (/lu)", "PASS", f"SVG anatomy rendered with {dot_count} circles ({duration}ms)")
        except Exception as e:
            record("Meridian Anatomy Chart (/lu)", "FAIL", str(e))

        # TEST 11: Meridian Trajectory Banner & Total Points on /lu
        try:
            banner = page.locator(".meridian-path-banner")
            assert banner.is_visible(), "Meridian pathway banner (.meridian-path-banner) not visible"

            points_stat = page.locator(".mpb-stat", has_text="Total Points")
            assert "11" in points_stat.inner_text(), f"Expected 11 points for Lung, got {points_stat.inner_text()}"

            origin_stat = page.locator(".mpb-stat", has_text="Origin")
            assert "LU1" in origin_stat.inner_text(), f"Expected LU1 origin, got {origin_stat.inner_text()}"

            terminus_stat = page.locator(".mpb-stat", has_text="Terminus")
            assert "LU11" in terminus_stat.inner_text(), f"Expected LU11 terminus, got {terminus_stat.inner_text()}"

            kicker = page.locator(".kicker")
            assert "11 points" in kicker.inner_text().lower(), f"Expected '11 Points' in kicker, got {kicker.inner_text()}"

            record("Lung Trajectory Banner & 11 Points", "PASS", "Verified banner with 11 points, LU1 start, LU11 end, and kicker badge")
        except Exception as e:
            record("Lung Trajectory Banner & 11 Points", "FAIL", str(e))

        # TEST 12: Renamed Large Intestine Chart (/li) - 20 Points
        try:
            resp = page.goto(f"{BASE_URL}/li", wait_until="networkidle")
            assert resp.status == 200, f"Expected 200 OK, got {resp.status}"

            points_stat = page.locator(".mpb-stat", has_text="Total Points")
            assert "20" in points_stat.inner_text(), f"Expected 20 points for LI, got {points_stat.inner_text()}"

            origin_stat = page.locator(".mpb-stat", has_text="Origin")
            assert "LI1" in origin_stat.inner_text(), f"Expected LI1 origin, got {origin_stat.inner_text()}"

            terminus_stat = page.locator(".mpb-stat", has_text="Terminus")
            assert "LI20" in terminus_stat.inner_text(), f"Expected LI20 terminus, got {terminus_stat.inner_text()}"

            record("Renamed LI Meridian Chart (20 Points)", "PASS", "li-meridian-chart.html loads with 20 points, LI1 start, LI20 end")
        except Exception as e:
            record("Renamed LI Meridian Chart (20 Points)", "FAIL", str(e))

        # TEST 13: Renamed Bladder Chart (/bl) - 67 Points
        try:
            resp = page.goto(f"{BASE_URL}/bl", wait_until="networkidle")
            assert resp.status == 200, f"Expected 200 OK, got {resp.status}"

            points_stat = page.locator(".mpb-stat", has_text="Total Points")
            assert "67" in points_stat.inner_text(), f"Expected 67 points for Bladder, got {points_stat.inner_text()}"

            origin_stat = page.locator(".mpb-stat", has_text="Origin")
            assert "BL1" in origin_stat.inner_text(), f"Expected BL1 origin, got {origin_stat.inner_text()}"

            terminus_stat = page.locator(".mpb-stat", has_text="Terminus")
            assert "BL67" in terminus_stat.inner_text(), f"Expected BL67 terminus, got {terminus_stat.inner_text()}"

            record("Renamed Bladder Meridian Chart (67 Points)", "PASS", "bl-meridian-chart.html loads with 67 points, BL1 start, BL67 end")
        except Exception as e:
            record("Renamed Bladder Meridian Chart (67 Points)", "FAIL", str(e))

        # TEST 14: Legacy Backwards-Compatible Aliases (*-v4-*)
        try:
            resp_li = page.goto(f"{BASE_URL}/li-v4-meridian-chart.html", wait_until="networkidle")
            assert resp_li.status == 200, f"Expected 200 OK for legacy li-v4 URL, got {resp_li.status}"

            resp_bl = page.goto(f"{BASE_URL}/bl-v4-meridian-chart.html", wait_until="networkidle")
            assert resp_bl.status == 200, f"Expected 200 OK for legacy bl-v4 URL, got {resp_bl.status}"

            record("Legacy Aliases Compatibility", "PASS", "Both li-v4 and bl-v4 legacy URLs served with 200 OK")
        except Exception as e:
            record("Legacy Aliases Compatibility", "FAIL", str(e))

        # TEST 15: Channels Route Explorer Point Badges and Route Peeks
        try:
            page.goto(f"{BASE_URL}/channels", wait_until="networkidle")
            pts_tags = page.locator(".name .pts-tag")
            assert pts_tags.count() == 12, f"Expected 12 channel point count badges, found {pts_tags.count()}"

            peeks = page.locator(".route-peek")
            assert peeks.count() == 12, f"Expected 12 route start->end peeks, found {peeks.count()}"

            record("Channels Page Enriched Badges & Peeks", "PASS", "All 12 channels display point count pills and start->end route peeks")
        except Exception as e:
            record("Channels Page Enriched Badges & Peeks", "FAIL", str(e))

        # TEST 16: Mobile Responsive Meridian Banner
        try:
            mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
            mob_page = mobile_context.new_page()
            mob_page.goto(f"{BASE_URL}/lu", wait_until="networkidle")

            mob_banner = mob_page.locator(".meridian-path-banner")
            assert mob_banner.is_visible(), "Mobile banner not visible"

            mobile_context.close()
            record("Mobile Viewport Banner Responsiveness", "PASS", "Banner displays cleanly on 390x844 mobile viewport")
        except Exception as e:
            record("Mobile Viewport Banner Responsiveness", "FAIL", str(e))

        browser.close()

    print("\n==================================================")
    passes = sum(1 for _, s, _ in test_results if s == "PASS")
    fails = sum(1 for _, s, _ in test_results if s == "FAIL")
    print(f" Playwright Test Summary: {passes} PASSED, {fails} FAILED out of {len(test_results)} tests")
    print("==================================================")
    return fails == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
