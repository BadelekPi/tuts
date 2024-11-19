import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        await page.set_viewport_size({'width': 1800, "height": 1200})
        await page.goto("https://demoqa.com/buttons")

        # Generic Click - Dynamic Selector
        button = page.locator("text=Click Me").nth(2)  # pick number from array of 3 elements
        await button.click()
        await page.screenshot(path="screenshots/dynamicClick.png")
        # Assertions
        await expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")

        # Double-Click
        button = page.locator("text=Click Me").nth(0)
        await button.dblclick()
        await page.screenshot(path="screenshots/doubleClick.png")
        # Assertions
        await expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")
        # Stop tracing
        await context.tracing.stop(path="logs/trace.zip")
        # Closing browser
        await browser.close()

asyncio.run(main())