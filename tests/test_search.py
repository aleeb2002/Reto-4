from playwright.sync_api import sync_playwright

BASE_URL = "https://demo.opencart.com"

def test_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # para diagnosticar
        context = browser.new_context(record_video_dir="test-results/videos")
        page = context.new_page()

        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="test-results/search_step1.png")

        page.wait_for_selector("input[name='search']", timeout=30000)
        page.fill("input[name='search']", "iPhone")
        page.screenshot(path="test-results/search_step2.png")

        page.click("#search button")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="test-results/search_step3.png")

        assert page.is_visible("text=iPhone")

        context.close()
        browser.close()
