import asyncio
from playwright.async_api import async_playwright
from src.parser import get_recipe_details
from src.utils import save_to_json
import time

async def count_api_requests(page, duration_minutes):
    # Initialize request counter
    api_request_count = 0

    # Define the request handler
    def on_request(request):
        nonlocal api_request_count
        if "/api/" in request.url or "recipe-ajax.php" in request.url:
            api_request_count += 1

    # Listen to all requests
    page.on("request", on_request)

    # Start the timer
    start_time = time.time()
    duration_seconds = duration_minutes * 60

    print(f"Monitoring API requests for {duration_minutes} minute(s)...")

    # Keep the script running for the specified duration
    while time.time() - start_time < duration_seconds:
        await asyncio.sleep(1)

    print(f"Total API requests made: {api_request_count}")

async def fetch_recipes(page, current_page):
    # Define the data to be sent in the POST request
    data = {
        'page': current_page,
        'ajaxAction': 'load_more_recipes',
        'search': ''
    }

    # Perform the AJAX POST request
    response = await page.evaluate("""
        async ({data}) => {
            const response = await fetch('https://ranveerbrar.com/wp-content/themes/ranveer-brar/recipe-ajax.php', {
                method: 'POST',
                body: new URLSearchParams(data),
            });
            return await response.text();
        }
    """, {"data": data})

    # Parse the returned HTML to get the recipe links
    return response

async def scrape_recipes():
    base_url = 'https://ranveerbrar.com/recipes/'
    all_recipes = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Start by loading the base URL
            await page.goto(base_url, timeout=60000)

            current_page = 1
            while True:
                print(f"Scraping page {current_page}")
                await count_api_requests(page, duration_minutes=1) # Change duration here as needed

                # Fetch the recipes using AJAX
                response_html = await fetch_recipes(page, current_page)

                # Load the response HTML into Playwright
                await page.set_content(response_html)

                # Extract the recipe links
                recipe_links = await page.eval_on_selector_all(
                    'div.rc_post > div.rc_thumb_wrap > a',
                    'elements => elements.map(e => e.href)'
                )
