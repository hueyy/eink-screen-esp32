from playwright.sync_api import sync_playwright  # type: ignore
from PIL import Image
import io
import os

CADDY_PORT = os.environ.get("CADDY_PORT", "8000")


def render_dashboard() -> bytes:
    """
    Returns screenshot as image buffer
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"http://localhost:{CADDY_PORT}/current_dashboard"
        print("Navigating to: ", url)
        try:
            page.goto(url, timeout=10000)
            screenshot = page.locator("main").screenshot()
            return screenshot
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            raise e
        finally:
            browser.close()


def image_buffer_to_bytes(image_buffer: bytes) -> bytes:
    with Image.open(io.BytesIO(image_buffer)) as img:
        # Convert to RGB mode
        img = img.convert("RGBA")
        # Get raw bytes
        return img.tobytes()


def bytes_to_image_buffer(
    raw_bytes: bytes, width: int = 800, height: int = 480
) -> bytes:
    img = Image.frombytes("RGBA", (width, height), raw_bytes)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
