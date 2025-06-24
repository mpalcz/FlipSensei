# FlipSensei

FlipSensei is a lightweight Chrome extension that scrapes listings from Facebook Marketplace and uses AI to assess whether an item is worth flipping.

## Features
- Scrapes product titles, prices, locations, and links from Marketplace
- Supports infinite scrolling with dynamic scraping via MutationObserver
- Uses AI (planned) to compare listing prices with online data to evaluate resale potential
- Logs results to the browser console

## AI-Powered Flipping Analysis (Planned)
The next phase of FlipSensei will use AI to:
- Identify underpriced items
- Estimate fair market value using external sources such as eBay or Amazon
- Recommend whether a product is likely to yield a profit if flipped

## How It Works
FlipSensei injects a content script into Facebook Marketplace pages and monitors the DOM for new listings as you scroll. When new product elements appear, it extracts data including the title, price, and link.

## Use Cases
- Product research for resale
- Marketplace flipping
- Personal finance tools
- Browser-based AI experimentation

## Project Status
- Scraping and infinite scroll handling are functional
- AI comparison and price valuation in progress
- Export and UI features planned for future updates

---