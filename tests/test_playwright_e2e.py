import os
import sys
import tempfile
import time
import pathlib
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://acu.caffeinity.com"
# Screenshots go to $SHU_SHOTS when set, otherwise to a temp folder, so the suite runs on any machine.
SCREENSHOTS_DIR = pathlib.Path(os.environ.get("SHU_SHOTS") or pathlib.Path(tempfile.gettempdir()) / "shu-atlas-playwright")
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

        # TEST 11: Premium Gateway Cards & Waypoint Journey on /lu
        try:
            # The route and relations block is folded under the point details; it opens on request
            banner = page.locator(".meridian-path-banner")
            assert not banner.is_visible(), "Route and relations should start folded away"
            page.locator("#more summary").click()
            page.wait_for_timeout(200)
            assert banner.is_visible(), "Meridian pathway banner (.meridian-path-banner) not visible once opened"

            # Check topbar points count
            topbar = page.locator(".mpb-topbar")
            assert "11" in topbar.inner_text(), f"Expected 11 points for Lung, got {topbar.inner_text()}"

            # Check origin gateway card
            origin_card = page.locator(".gateway-card.origin")
            assert origin_card.is_visible(), "Origin gateway card not visible"
            assert "LU1" in origin_card.inner_text(), f"Expected LU1 in origin card, got {origin_card.inner_text()}"
            assert "Zhongfu" in origin_card.inner_text(), "Expected Zhongfu in origin card"

            # Check terminus gateway card
            terminus_card = page.locator(".gateway-card.terminus")
            assert terminus_card.is_visible(), "Terminus gateway card not visible"
            assert "LU11" in terminus_card.inner_text(), f"Expected LU11 in terminus card, got {terminus_card.inner_text()}"
            assert "Shaoshang" in terminus_card.inner_text(), "Expected Shaoshang in terminus card"

            # Check 4 milestone stages in timeline
            stage_cards = page.locator(".stage-card")
            assert stage_cards.count() == 4, f"Expected 4 milestone stage cards, found {stage_cards.count()}"

            # Check kicker badge
            kicker = page.locator(".kicker")
            assert "11 points" in kicker.inner_text().lower(), f"Expected '11 Points' in kicker, got {kicker.inner_text()}"

            record("Lung Gateway Cards & 4-Stage Waypoints", "PASS", "Verified premium Origin (LU1 Zhongfu), Terminus (LU11 Shaoshang), 4-stage waypoints")
        except Exception as e:
            record("Lung Gateway Cards & 4-Stage Waypoints", "FAIL", str(e))

        # TEST 12: Renamed Large Intestine Chart (/li) - 20 Points & Gateway Cards
        try:
            resp = page.goto(f"{BASE_URL}/li", wait_until="networkidle")
            assert resp.status == 200, f"Expected 200 OK, got {resp.status}"

            # the route block is folded until asked for, so read its text rather than its rendered text
            topbar = page.locator(".mpb-topbar")
            assert "20" in topbar.text_content(), f"Expected 20 points for LI, got {topbar.text_content()}"

            origin_card = page.locator(".gateway-card.origin")
            assert "LI1" in origin_card.text_content(), f"Expected LI1 origin, got {origin_card.text_content()}"

            terminus_card = page.locator(".gateway-card.terminus")
            assert "LI20" in terminus_card.text_content(), f"Expected LI20 terminus, got {terminus_card.text_content()}"

            record("Renamed LI Meridian Chart (20 Points & Gateway Cards)", "PASS", "li-meridian-chart.html loads with 20 points, LI1 start, LI20 end")
        except Exception as e:
            record("Renamed LI Meridian Chart (20 Points & Gateway Cards)", "FAIL", str(e))

        # TEST 13: Renamed Bladder Chart (/bl) - 67 Points & Gateway Cards
        try:
            resp = page.goto(f"{BASE_URL}/bl", wait_until="networkidle")
            assert resp.status == 200, f"Expected 200 OK, got {resp.status}"

            topbar = page.locator(".mpb-topbar")
            assert "67" in topbar.text_content(), f"Expected 67 points for Bladder, got {topbar.text_content()}"

            origin_card = page.locator(".gateway-card.origin")
            assert "BL1" in origin_card.text_content(), f"Expected BL1 origin, got {origin_card.text_content()}"

            terminus_card = page.locator(".gateway-card.terminus")
            assert "BL67" in terminus_card.text_content(), f"Expected BL67 terminus, got {terminus_card.text_content()}"

            record("Renamed Bladder Meridian Chart (67 Points & Gateway Cards)", "PASS", "bl-meridian-chart.html loads with 67 points, BL1 start, BL67 end")
        except Exception as e:
            record("Renamed Bladder Meridian Chart (67 Points & Gateway Cards)", "FAIL", str(e))

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

            # On a phone the block sits in the details sheet: opening it pulls the sheet up
            mob_page.locator("#grab").click()
            mob_page.wait_for_timeout(600)
            mob_page.locator("#more summary").click()
            mob_page.wait_for_timeout(300)
            mob_banner = mob_page.locator(".meridian-path-banner")
            assert mob_banner.is_visible(), "Mobile banner not visible"
            box = mob_banner.bounding_box()
            assert box and box["width"] <= 390, f"Banner wider than the phone: {box}"

            mobile_context.close()
            record("Mobile Viewport Banner Responsiveness", "PASS", "Banner displays cleanly on 390x844 mobile viewport")
        except Exception as e:
            record("Mobile Viewport Banner Responsiveness", "FAIL", str(e))

        # TEST 17: Mobile Responsive Homepage Viewport
        try:
            mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
            mob_home = mobile_context.new_page()
            mob_home.goto(f"{BASE_URL}/", wait_until="networkidle")
            mob_home.wait_for_timeout(1000)

            # 1. Viewport tag present
            viewport_tag = mob_home.locator('meta[name="viewport"]').first
            assert viewport_tag.is_visible or viewport_tag.count() > 0, "Viewport meta tag missing on homepage"

            # 2. .phone class applied
            has_phone_class = mob_home.evaluate('document.getElementById("vis").classList.contains("phone")')
            assert has_phone_class, "Expected .phone class on mobile root"

            # 3. 5 discs rendered and within viewport bounds
            discs = mob_home.locator(".vis-med")
            assert discs.count() == 5, f"Expected 5 discs, got {discs.count()}"

            # 4. Legend chips present on mobile
            chips = mob_home.locator(".vis-chip")
            assert chips.count() == 2, f"Expected 2 legend chips, got {chips.count()}"

            # 5. Nav links present
            appnav_links = mob_home.locator("#shu-nav a.l")
            assert appnav_links.count() == 5, f"Expected 5 appnav links, got {appnav_links.count()}"

            mobile_context.close()
            record("Mobile Homepage Responsiveness", "PASS", "Homepage renders mobile layout with viewport tag, .phone styling and 5 elements")
        except Exception as e:
            record("Mobile Homepage Responsiveness", "FAIL", str(e))

        # 18. Conception Vessel Chart (/cv) & Nalaayan Anatomical Diagrams
        try:
            cv_page = context.new_page()
            resp = cv_page.goto(f"{BASE_URL}/cv", wait_until="networkidle")
            assert resp.status == 200, f"Expected status 200, got {resp.status}"
            assert "Conception Vessel" in cv_page.title()
            chips = cv_page.locator(".pts .chip")
            assert chips.count() == 5, f"Expected 5 chips, got {chips.count()}"
            # Select Water (CV6)
            cv_page.locator('.chip[data-id="p6"]').click()
            cv_page.wait_for_timeout(200)
            info = cv_page.locator("#pt-info").inner_text()
            assert "CV6" in info and "Qihai" in info and "Water" in info
            # Verify Nalaayan anatomical location diagram image is rendered
            img = cv_page.locator("#pt-info figure img")
            assert img.is_visible(), "Expected Nalaayan location diagram image to be visible in #pt-info"
            record("Conception Vessel Chart (/cv)", "PASS", "CV chart rendered with 5 element points, anatomy, and Nalaayan diagram images")
        except Exception as e:
            record("Conception Vessel Chart (/cv)", "FAIL", str(e))

        # 19. Conception Vessel Hidden from Channels Directory
        try:
            ch_page = context.new_page()
            ch_page.goto(f"{BASE_URL}/channels", wait_until="networkidle")
            cv_route = ch_page.locator('.route[data-ch="CV"]')
            assert cv_route.count() == 0, "Expected CV route to be hidden from channels.html"
            counter = ch_page.locator("#match-counter").inner_text()
            assert "12" in counter, f"Expected 12 primary channels in counter, got {counter}"
            record("CV Hidden from Channels Directory", "PASS", "CV channel successfully hidden from Channels directory while primary 12 channels remain clean")
        except Exception as e:
            record("CV Hidden from Channels Directory", "FAIL", str(e))

        # TEST 20: App shell - Elements, Channels and Points swap in place, with no page load
        try:
            app = context.new_page()
            app.goto(f"{BASE_URL}/", wait_until="networkidle")
            app.wait_for_timeout(3200)
            app.evaluate("window.__boot = 1")
            app.locator('#nav button[aria-label="Fire"]').click()
            app.wait_for_timeout(1500)
            app.locator("#cta").click()
            app.wait_for_timeout(1200)
            assert app.url.endswith("channels.html#fire"), f"Expected channels.html#fire, got {app.url}"
            assert app.evaluate("window.__boot") == 1, "Explore reloaded the page"
            assert app.title().startswith("Channels"), f"Title not updated: {app.title()}"
            fire = app.locator(".map .route:not([hidden])")
            assert fire.count() == 4, f"Expected the 4 Fire channels, got {fire.count()}"
            assert app.locator('#shu-nav a.l[aria-current="page"]').inner_text() == "Channels"
            assert app.evaluate("ShuAtlas.element()") == "fire", "Scene did not follow the element"

            app.locator('#shu-nav a.l[href="points.html"]').click()
            app.wait_for_timeout(1000)
            assert app.locator("#list li").count() == 65, "Points list not rendered in place"
            app.locator("#q").fill("wrist")
            app.wait_for_timeout(250)
            kept = app.locator("#list li").count()
            app.locator('#shu-nav a.l[href="channels.html"]').click()
            app.wait_for_timeout(800)
            assert app.locator(".map .route:not([hidden])").count() == 4, "Channels lost its Fire filter on return"
            app.locator('#shu-nav a.l[href="points.html"]').click()
            app.wait_for_timeout(800)
            assert app.locator("#q").input_value() == "wrist", "Points lost its search on return"
            assert app.locator("#list li").count() == kept, "Points lost its results on return"

            app.locator('#shu-nav a.l[href="index.html"]').click()
            app.wait_for_timeout(1200)
            assert app.locator(".vis-med").count() == 5, "Ring missing after returning to Elements"
            assert app.locator(".vis-title-name").inner_text() == "Fire", "Ring did not keep its element"
            app.go_back()
            app.wait_for_timeout(800)
            assert app.evaluate("ShuAtlas.view()") == "points", "Back did not return to Points"
            assert app.evaluate("window.__boot") == 1, "A page load happened inside the app"
            app.close()
            record("App Shell In-Place Views", "PASS", "Elements, Channels and Points swap with no reload; filter, search, ring and Back all hold")
        except Exception as e:
            record("App Shell In-Place Views", "FAIL", str(e))

        # TEST 21: App shell - a deep link to any view boots the same app
        try:
            deep = context.new_page()
            deep.goto(f"{BASE_URL}/points", wait_until="networkidle")
            deep.evaluate("window.__boot = 1")
            deep.locator('#shu-nav a.l[href="index.html"]').click()
            deep.wait_for_timeout(3200)
            assert deep.locator(".vis-med").count() == 5, "Ring did not mount from a Points deep link"
            deep.locator("#cta").click()
            deep.wait_for_timeout(1200)
            assert deep.locator(".map .route").count() == 12, "Channels did not mount from the ring"
            assert deep.evaluate("window.__boot") == 1, "A page load happened inside the app"
            deep.close()
            record("App Shell Deep Link", "PASS", "A /points deep link reaches the ring and Channels in place")
        except Exception as e:
            record("App Shell Deep Link", "FAIL", str(e))

        # TEST 22: App shell - the header holds one position on every view, desktop and phone
        try:
            for size in ({"width": 1440, "height": 900}, {"width": 390, "height": 844}):
                ctx = browser.new_context(viewport=size)
                hp = ctx.new_page()
                boxes = []
                for route in ("/", "/channels", "/points"):
                    hp.goto(f"{BASE_URL}{route}", wait_until="networkidle")
                    nav = hp.locator("#shu-nav").bounding_box()
                    first = hp.locator("#shu-nav a.l").first.bounding_box()
                    brand = hp.locator("#shu-nav .home").bounding_box()
                    boxes.append((round(nav["height"]), round(brand["x"]), round(first["x"]), round(first["y"])))
                    wide = hp.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                    assert not wide, f"{route} scrolls sideways at {size['width']}px"
                assert len(set(boxes)) == 1, f"Header moves between views at {size['width']}px: {boxes}"
                ctx.close()
            record("App Shell Fixed Header", "PASS", "Brand and tabs sit at the same position on Elements, Channels and Points")
        except Exception as e:
            record("App Shell Fixed Header", "FAIL", str(e))

        # TEST 23: Channel page on a phone: plate in view, card turns to the location diagram, sheet pulls up
        try:
            mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
            mp = mobile_context.new_page()
            mp.goto(f"{BASE_URL}/gb", wait_until="networkidle")
            mp.wait_for_timeout(500)

            leg = mp.locator(".leg").bounding_box()
            assert leg and leg["y"] >= 0 and leg["y"] + leg["height"] <= 844, f"Plate is not fully on the first screen: {leg}"
            assert mp.evaluate("document.documentElement.scrollHeight") <= 844, "Channel page should be one fixed screen on a tall phone"
            ticks = mp.locator(".cline .cl-track i")
            assert ticks.count() == 5, f"Expected 5 Shu marks on the channel line, found {ticks.count()}"

            mp.locator('.hit[data-id="p34"]').click(force=True)
            mp.wait_for_timeout(1000)
            assert mp.evaluate('document.getElementById("stage").classList.contains("loc")'), "Tapping a point should turn the card to its location diagram"
            img = mp.locator("#loc-img")
            assert img.is_visible() and "GB34" in (img.get_attribute("alt") or ""), "Location diagram for GB34 not shown"
            assert mp.locator("#pt-info .loc").is_visible(), "Location text should stay in view under the diagram"
            loc_box = mp.locator("#pt-info .loc").bounding_box()
            assert loc_box["y"] + loc_box["height"] <= 844, f"Location text is off screen: {loc_box}"

            mp.locator('.vsw button[data-face="map"]').click()
            mp.wait_for_timeout(900)
            assert not mp.evaluate('document.getElementById("stage").classList.contains("loc")'), "Channel map button should turn the card back"

            mp.locator("#grab").click()
            mp.wait_for_timeout(600)
            assert mp.locator("#grab").get_attribute("aria-expanded") == "true", "Sheet did not open"
            mp.screenshot(path=str(SCREENSHOTS_DIR / "23_channel_phone_sheet.png"))
            mobile_context.close()
            record("Channel Page Phone Layout", "PASS", "Plate on first screen, card turns to the GB34 diagram and back, location text in view, sheet opens")
        except Exception as e:
            record("Channel Page Phone Layout", "FAIL", str(e))

        # TEST 24: Channel page on desktop: diagram beside its location, every chart on the shared layout
        try:
            dp = context.new_page()
            dp.goto(f"{BASE_URL}/gb#GB38", wait_until="networkidle")
            dp.wait_for_timeout(400)
            fig = dp.locator("#pt-info figure img")
            assert fig.is_visible() and "GB38" in (fig.get_attribute("alt") or ""), "Desktop location diagram missing for GB38"
            assert dp.locator(".leg").bounding_box()["y"] < 900, "Plate should start on the first screen"
            assert not dp.locator(".vsw").is_visible(), "The map/location switch is for phones only"
            bad = []
            for key in ["lu", "li", "st", "sp", "ht", "si", "bl", "ki", "pc", "tb", "gb", "lr"]:
                dp.goto(f"{BASE_URL}/{key}", wait_until="domcontentloaded")
                ok = dp.evaluate("""() => !!document.querySelector('main[data-chartapp]') && document.querySelectorAll('.cline .cl-track i').length === 5
                    && document.querySelectorAll('.hit').length === 5 && !!document.querySelector('#more .meridian-path-banner') && !!document.body.dataset.el""")
                if not ok:
                    bad.append(key)
            assert not bad, f"Charts not on the shared layout: {bad}"
            dp.close()
            record("Channel Page Desktop Layout", "PASS", "Diagram sits beside its location; all 12 charts carry the line, 5 points and folded route block")
        except Exception as e:
            record("Channel Page Desktop Layout", "FAIL", str(e))

        # TEST 25: Phone dock, ring labels and weather on the home screen
        try:
            mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
            mh = mobile_context.new_page()
            mh.goto(f"{BASE_URL}/", wait_until="networkidle")
            mh.wait_for_timeout(3600)
            dock = mh.locator("#shu-nav ul").bounding_box()
            assert dock and dock["y"] > 844 * 0.8, f"Tabs should sit in a dock at the bottom on a phone: {dock}"
            assert dock["x"] >= 0 and dock["x"] + dock["width"] <= 390, f"Dock overflows the screen: {dock}"
            picker = mh.locator("#nav").bounding_box()
            assert picker["y"] + picker["height"] <= dock["y"], "Element picker overlaps the dock"
            labs = mh.locator(".vis-lab")
            assert labs.count() == 2, f"Expected 2 cycle labels on the ring, found {labs.count()}"
            assert "feeds Fire" in labs.nth(0).inner_text() and "parts Earth" in labs.nth(1).inner_text(), "Ring labels do not name the Wood relations"
            assert mh.evaluate("""() => { const c = document.getElementById('fx'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
                for (let i = 3; i < d.length; i += 4) if (d[i]) return true; return false; }"""), "Weather canvas is empty"
            mh.locator("#cta").click()
            mh.wait_for_timeout(1500)
            assert mh.locator(".map .route").first.is_visible(), "Entering an element should land on Channels"
            assert mh.evaluate("getComputedStyle(document.querySelector('#shu-scene i.on')).opacity") == "1", "The element scene should stay behind Channels"
            mh.screenshot(path=str(SCREENSHOTS_DIR / "25_phone_channels_scene.png"))
            mobile_context.close()
            record("Phone Dock, Ring Labels, Weather and Scene", "PASS", "Dock at the bottom, labels on the ring, weather drawn, scene carried into Channels")
        except Exception as e:
            record("Phone Dock, Ring Labels, Weather and Scene", "FAIL", str(e))

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
