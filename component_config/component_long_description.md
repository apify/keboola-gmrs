# Google Maps Reviews data integration component

This component enables data teams to extract customer reviews from Google Maps locations into structured data formats suitable for ETL pipelines, data warehouses, and analytics platforms. Built on Apify's Google Maps Reviews Actor, this component delivers reliable data feeds for business intelligence and customer analytics applications.

## Data engineering use cases

- **Incremental data loading**: Schedule regular extractions with date filtering to implement efficient incremental loading patterns.
- **Data warehouse integration**: Feed review data directly into Keboola.
- **Customer experience analytics**: Build comprehensive customer sentiment analysis dashboards.
- **Multi-location business intelligence**: Compare performance metrics across different business locations.
- **Competitive analysis**: Gather standardized review data for competitors' locations to benchmark performance.

## Extracted data attributes

The component extracts and structures the following data points:

- Review text content and star ratings.
- Timestamps and publication dates.
- Owner responses to reviews.
- Service-specific ratings (where available).
- Review images metadata.
- Reviewer information (configurable based on privacy requirements).
- Review URLs and identifiers for cross-referencing.

## Integration patterns

Implement standard ETL/ELT workflows:

1. **Extract**: Configure the component to pull reviews data based on place URLs or IDs.
2. **Transform**: Process and normalize the extracted data to match your schema requirements.
3. **Load**: Import the structured data into your data warehouse.
4. **Analyze**: Join with internal data sources to create comprehensive business intelligence views.

## Configuration options

Fine-tune your data extraction with options including:

- Volume controls to manage data processing requirements.
- Sorting algorithms to prioritize most relevant content.
- Date filtering for incremental loading scenarios.
- Language preferences for consistent text analytics.
- Privacy controls for personal data compliance.

## Data governance and compliance

The component provides configuration options to control personal data extraction. Enable reviewer data extraction only when permitted by your data governance policies and ensure compliance with relevant data protection regulations, including GDPR for European Union data subjects.

## Getting your Apify token

To get started, create an account at console.apify.com. You can sign up using your email, Gmail, or GitHub account. You need to get the API token from your Apify account. Head over to Settings → API & Integrations tab to find API tokens at console.apify.com/settings/integrations. Find your token under Personal API tokens. Alternatively, you can also create a new API token with multiple customizable permissions by clicking on + Create a new token. Then copy this token and you can use it in Keboola.
