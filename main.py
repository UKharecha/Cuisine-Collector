import asyncio
from src.scraper import scrape_recipes

if __name__ == '__main__':
    asyncio.run(scrape_recipes())
