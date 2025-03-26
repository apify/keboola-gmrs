"""
Template Component main class.

"""
import csv
import logging
from apify_client import ApifyClient

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from configuration import Configuration

ACTOR_ID = 'Xb8osYTtOjlsgI6k9'


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Main execution code
        """

        # ####### EXAMPLE TO REMOVE
        # check for missing configuration parameters
        params = Configuration(**self.configuration.parameters)

        # get input table definitions
        input_tables = self.get_input_tables_definitions()
        for table in input_tables:
            logging.info(f'Received input table: {table.name} with path: {table.full_path}')

        if len(input_tables) == 0:
            raise UserException("No input tables found")

        place_ids = []
        start_urls = []
        # Add timestamp column and save into out_table_path
        for input_table in input_tables:
            with open(input_table.full_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                # columns = list(csv_reader.fieldnames)
                for row in csv_reader:
                    if row.get('place_id'):
                        place_ids.append(row['place_id'])
                    elif row.get('place_url'):
                        start_urls.append({ 'url': row['place_url'] })

        if len(place_ids) == 0 and len(start_urls) == 0:
            raise Exception('Didn\'t find any place IDs nor URLs')

        run_input = {
            'language': params.language,
            'maxReviews': params.maxReviews,
            'personalData': params.personalData,
            'reviewsOrigin': params.reviewsOrigin,
            'reviewsSort': params.reviewsSort,
            'placeIds': place_ids,
            'startUrls': start_urls,
        }
        if params.reviewsStartDate:
            run_input['reviewsStartDate'] = params.reviewsStartDate

        print(run_input)

        apify_client = ApifyClient(params.token)
        actor_client = apify_client.actor(ACTOR_ID)
        actor_run = actor_client.call(run_input = run_input)
        if not actor_run:
            raise Exception('Received empty run response')
        dataset_client = apify_client.dataset(actor_run['defaultDatasetId'])
        reviews = dataset_client.list_items().items

        output_columns = [
            'reviewerId',
            'reviewerUrl',
            'name',
            'reviewerNumberOfReviews',
            'isLocalGuide',
            'reviewerPhotoUrl',
            'reviewId',
            'text',
            'originalLanguage',
            'textTranslated',
            'translatedLanguage',
            'publishAt',
            'publishedAtDate',
            'likesCount',
            'reviewUrl',
            'reviewOrigin',
            'responseFromOwnerDate',
            'responseFromOwnerText',
            'reviewImageUrls',
            'reviewContext',
            'reviewDetailedRating',
            'visitedIn',
            'placeId',
            'title',
            'stars',
            'rating',
            'totalScore',
            'url',
            'cid',
            'fid',
            'searchString',
        ]

        output_table = self.create_out_table_definition('output.csv', incremental=True)
        for col in output_columns:
            output_table.add_column(col)
        self.write_manifest(output_table)

        with open(output_table.full_path, 'w') as file:
            csv_writer = csv.DictWriter(file, output_columns)
            rows = []
            for review in reviews:
                row = {}
                for col in output_columns:
                    row[col] = review.get(col)
                rows.append(row)
            csv_writer.writeheader()
            csv_writer.writerows(rows)


if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
