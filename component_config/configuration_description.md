The componnet expects an input table with one of the following columns:
- `place_id`: ID of a Google Maps place whose reviews to scrape
- `place_url`: URL of a Google maps place whose reviews to scrape

If both columns are present, `place_id` takes precedence.

Additionally, you can set the following options:
- number of reviews to scrape for each place
- language, in which the reviews will be scraped
- sorting: newest, most relevant, highest or lowest rating
- whether you want to scrape only reviews from Google or from other as well (e.g. Tripadvisor)
- date of the oldest review - the scraper will scrape only reviews newer than the selected date
