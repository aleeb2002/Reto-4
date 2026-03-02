from playwright.sync_api import sync_playwright
from test_login import create_context, goto_or_fail_on_challenge

def test_checkout_navigation():
    with sync_playwright() as p:
        browser, context = create_context(p, headless=False)
        page = context.new_page()

        goto_or_fail_on_challenge(page)
        page.screenshot(path="test-results/checkout_step1.png")

        page.click("a.ico-cart")
        page.wait_for_load_state("domcontentloaded")
        page.screenshot(path="test-results/checkout_step2.png")

        assert page.is_visible("div.page.shopping-cart-page")

        context.close()
        browser.close()