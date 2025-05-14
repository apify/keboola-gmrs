This Google Maps Reviews App extracts reviews data from Google Maps places to integrate into your data warehouse or analytics pipeline. You can extract review text, ratings, timestamps, reviewer details, and owner responses for customer sentiment analysis, competitive intelligence, and reputation management.

The component requires an input table with either:
* column containing Google Maps place URLs (default `place_url`) (containing /maps/search, /maps/place, or /maps/reviews).
* column containing Google Place IDs (default `place_id`) for the locations you want to analyze.

You can configure extraction parameters including review count limits, sorting methods, date filters, and language preferences to create customized data feeds for your analytics.

In order to start the actor, you need to provide Apify API Token, which you can get in [Apify's Settings](https://console.apify.com/settings/integrations).
