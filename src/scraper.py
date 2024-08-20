import asyncio
from playwright.async_api import async_playwright
from src.parser import get_recipe_details
from src.utils import save_to_json

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

                # Fetch the recipes using AJAX
                response_html = await fetch_recipes(page, current_page)

                # Load the response HTML into Playwright
                await page.set_content(response_html)

                # Extract the recipe links
                recipe_links = await page.eval_on_selector_all(
                    'div.rc_post > div.rc_thumb_wrap > a',
                    'elements => elements.map(e => e.href)'
                )

                if not recipe_links:
                    print("No more recipes found.")
                    break

                for link in recipe_links:
                    recipe = await get_recipe_details(page, link)
                    if recipe:
                        all_recipes.append(recipe)

                current_page += 1

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

    save_to_json('data/processed/recipes.json', all_recipes)

if __name__ == '__main__':
    asyncio.run(scrape_recipes())
