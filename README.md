# 🍽️ Cuisine Collector

**Cuisine Collector** is a Python-based web scraping tool designed to extract and compile detailed recipe information from culinary websites. 🍲 Using the Playwright library, this project automates browser interactions to gather recipe details like titles, ingredients, and cooking instructions. 📜

## Key Features

- **Automated Recipe Extraction**: Scrape recipes from specified websites effortlessly. 🚀
- **Comprehensive Data Collection**: Retrieve titles, ingredients, and cooking processes. 📝
- **Customizable**: Adapt easily to different recipe sites by modifying selectors. 🔧
- **Output in JSON Format**: Save collected recipes in a structured JSON file for easy use and analysis. 📂

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/UKharecha/Cuisine-Collector.git
    ```

2. Navigate to the project directory:
    ```bash
    cd CuisineCollector
    ```

3. Install the required dependencies:
    ```bash
    pip install playwright
    playwright install

    ```

## Usage

1. Update the `scraper.py` file with the target website and appropriate selectors. 🛠️
2. Run the scraper:
    ```bash
    python main.py
    ```

3. Check the `data/processed/recipes.json` file for the extracted recipe data. 📁

## Contribution

We welcome contributions! 🎉 Feel free to submit issues or pull requests. 🤝

---

Happy scraping! 🍴
