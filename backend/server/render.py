from playwright.sync_api import sync_playwright  # type: ignore
from PIL import Image
import io


def render_dashboard() -> bytes:
    """
    Returns screenshot as image buffer
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000/current_dashboard")
        screenshot = page.locator("main").screenshot()
        browser.close()
        return screenshot


def image_buffer_to_bytes(image_buffer: bytes):
    with Image.open(io.BytesIO(image_buffer)) as img:
        # Convert to RGB mode
        img = img.convert("RGBA")
        # Get raw bytes
        return img.tobytes()


def render_dashboard_as_rgb() -> bytes:
    screenshot_buffer = render_dashboard()
    return image_buffer_to_bytes(screenshot_buffer)
