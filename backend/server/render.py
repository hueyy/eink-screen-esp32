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
