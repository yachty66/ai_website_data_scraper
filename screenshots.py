import asyncio
import os
from playwright.async_api import async_playwright

async def capture_screenshots(url, output_folder, viewport_width=1920, viewport_height=1080):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    async with async_playwright() as p:
        # Launch the browser in headless mode
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height}
        )
        page = await context.new_page()

        # Navigate to the URL
        await page.goto(url, wait_until='networkidle')
        await asyncio.sleep(2)  # Wait for additional content to load

        # Get the total page dimensions
        total_width = await page.evaluate("() => document.body.scrollWidth")
        total_height = await page.evaluate("() => document.body.scrollHeight")

        print(f"Page dimensions: {total_width}px width x {total_height}px height")

        # Calculate the number of screenshots needed
        columns = total_width // viewport_width + (1 if total_width % viewport_width else 0)
        rows = total_height // viewport_height + (1 if total_height % viewport_height else 0)

        print(f"Capturing {rows} rows x {columns} columns of screenshots.")

        for row in range(rows):
            for col in range(columns):
                scroll_x = col * viewport_width
                scroll_y = row * viewport_height

                # Scroll to the position
                await page.evaluate(f"window.scrollTo({scroll_x}, {scroll_y})")
                await asyncio.sleep(0.5)  # Wait for the scroll

                # Capture the screenshot
                screenshot_path = os.path.join(output_folder, f"screenshot_{row}_{col}.png")
                await page.screenshot(path=screenshot_path, full_page=False)
                print(f"Saved {screenshot_path}")

        await browser.close()

def main(url):
    output_dir = "screenshots"
    asyncio.run(capture_screenshots(url, output_dir))

if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    main(url)