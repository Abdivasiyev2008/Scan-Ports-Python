import asyncio
from pyppeteer import launch


async def take_screenshot(url, path):
    # Launch a new headless browser instance
    browser = await launch()
    # Open a new page
    page = await browser.newPage()
    # Navigate to the website
    await page.goto(url)
    # Take a screenshot and save it to a file
    await page.screenshot({'path': path})
    # Close the browser
    await browser.close()


# URL of the website and path to save the screenshot
# try:
#     url = 'http://94.228.116.48'
#     screenshot_path = 'screenshot.png'
#
#     # Run the asynchronous function
#     asyncio.get_event_loop().run_until_complete(take_screenshot(url, screenshot_path))
#
#     print(f"Screenshot saved to {screenshot_path}")
#
# except Exception as e:
#     print(e)
