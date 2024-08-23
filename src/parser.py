async def get_recipe_details(page, url):
    print(f"Scraping URL: {url}")
    await page.goto(url)

    try:
        # Use a more generalized selector for the title
        title_element = await page.query_selector('h1')
        title = await title_element.text_content()
        title = title.strip() if title else "No Title Found"
        print(f"Title: {title}")
    except Exception as e:
        print(f"Error getting title: {e}")
        title = "No Title Found"

    ingredients_sections = await page.query_selector_all('div.ingredients_cont_wrap > p')

    ingredients = []
    for section in ingredients_sections:
        ingredient = await section.text_content()
        ingredients.append(ingredient.strip())
        print(f"Ingredients: {ingredients}")

    process_sections = await page.query_selector_all('div.process_wrap > div.process_inner_wrap > ul')

    process = []
    for section in process_sections:
        steps = await section.inner_html()
        process.append(steps.strip())
        print(f"Process: {process}")
