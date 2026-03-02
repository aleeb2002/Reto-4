from playwright.sync_api import sync_playwright
from test_login import create_context, goto_or_fail_on_challenge

def test_add_to_cart():
    with sync_playwright() as p:
        browser, context = create_context(p, headless=False)
        page = context.new_page()

        goto_or_fail_on_challenge(page)
        page.screenshot(path="test-results/cart_step1.png")

        page.wait_for_selector("input#small-searchterms", timeout=30000)
        page.fill("input#small-searchterms", "Laptop")
        page.click("button.search-box-button")

        page.wait_for_selector("h2.product-title a", timeout=30000)
        page.screenshot(path="test-results/cart_step2.png")

        # Abre el primer producto
        page.click("h2.product-title a")
        page.wait_for_load_state("domcontentloaded")
        page.screenshot(path="test-results/cart_step3.png")

        # Botón add-to-cart puede variar por producto.
        # En nopCommerce demo suele ser button#add-to-cart-button-<id>
        page.wait_for_selector("button[id^='add-to-cart-button-']", timeout=30000)
        page.click("button[id^='add-to-cart-button-']")
        page.wait_for_timeout(1000)
        page.screenshot(path="test-results/cart_step4.png")

        # Validación: aparece alguna notificación/barra de éxito
        assert page.locator("div.bar-notification").is_visible()

        context.close()
        browser.close()