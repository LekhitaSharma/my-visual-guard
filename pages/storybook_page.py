from playwright.sync_api import Page

class StorybookPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def open(self, story_id: str, theme: str = "light"):
        url = f"{self.base_url}/iframe.html?id={story_id}&globals=theme:{theme}"
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_selector("#storybook-root")
        return self.page.locator("#storybook-root")
