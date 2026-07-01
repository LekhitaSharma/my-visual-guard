import pytest

# Use Playwright's own demo site - never blocks, always up
DEMO_URL = "https://demo.playwright.dev"

@pytest.fixture(params=["light", "dark"])
def theme(request, page):
    # inject theme via prefers-color-scheme
    theme = request.param
    page.emulate_media(color_scheme=theme)
    return theme

@pytest.fixture(params=[375, 768, 1440], ids=["mobile","tablet","desktop"])
def viewport_width(request, page):
    w = request.param
    page.set_viewport_size({"width": w, "height": 800})
    return w

@pytest.fixture
def goto_demo(page):
    def _goto(path="/todomvc"):
        page.goto(f"{DEMO_URL}{path}", wait_until="domcontentloaded")
        page.wait_for_timeout(300)
    return _goto
