from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

BASE_URL = "https://demo.nopcommerce.com/"

def create_context(p, headless=False):
    browser = p.chromium.launch(
        headless=headless,
        args=[
            "--start-maximized",
            "--disable-features=IsolateOrigins",
            "--disable-site-isolation-trials",
        ],
    )

    context = browser.new_context(
        record_video_dir="test-results/videos",
        ignore_https_errors=True,
        viewport=None,
        locale="es-ES",
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
    )
    return browser, context

def goto_or_fail_on_challenge(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(800)

    # Si Cloudflare / challenge aparece, normalmente NO existe el search box.
    # Esto te deja un error claro en vez de un timeout confuso.
    if page.locator("text=Performing security verification").is_visible(timeout=1000) \
       or page.locator("text=Checking your browser").is_visible(timeout=1000):
        page.screenshot(path="test-results/challenge_detected.png")
        raise AssertionError(
            "El sitio mostró verificación anti-bot (Cloudflare). "
            "No se puede automatizar mientras esa pantalla aparezca."
        )

def test_login_smoke():
    with sync_playwright() as p:
        browser, context = create_context(p, headless=False)
        page = context.new_page()

        goto_or_fail_on_challenge(page)
        page.screenshot(path="test-results/login_step1.png")

        page.click("a.ico-login")
        page.wait_for_selector("#Email", timeout=30000)
        page.wait_for_selector("#Password", timeout=30000)
        page.screenshot(path="test-results/login_step2.png")

        # Smoke check: la pantalla de login existe y tiene sus campos/botón
        assert page.is_visible("button.login-button")

        context.close()
        browser.close()
