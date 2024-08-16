import asyncio
from playwright.async_api import async_playwright
from src.parser import get_recipe_details
from src.utils import save_to_json


async def scrape_recipes():
    base_url = 'https://ranveerbrar.com/recipes/'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto(base_url, timeout=60000)

            await page.wait_for_selector('div.recipe-content.row > div > article > div > div > a')

            # Get all recipe links
            recipe_links = await page.eval_on_selector_all(
                'div.recipe-content.row > div > article > div > div > a',
                'elements => elements.map(e => e.href)'
            )

            all_recipes = []
            for link in recipe_links:
                recipe = await get_recipe_details(page, link)
                if recipe:
                    all_recipes.append(recipe)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

    save_to_json('data/processed/recipes.json', all_recipes)


if __name__ == '__main__':
    asyncio.run(scrape_recipes())
