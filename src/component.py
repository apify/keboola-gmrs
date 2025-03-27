"""
Template Component main class.

"""
import csv
import logging
from apify_client import ApifyClient

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

from configuration import Configuration
from consts import ACTOR_ID, OUTPUT_COLUMNS, REQUIRED_PARAMETERS

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
        # check for missing configuration parameters
        self.validate_configuration_parameters(mandatory_params=REQUIRED_PARAMETERS)
        params = Configuration(**self.configuration.parameters)

        place_ids, start_urls = self.read_input_table() 

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

        apify_client = ApifyClient(params.token)
        actor_client = apify_client.actor(ACTOR_ID)

        try:
            # Validate that the token is working
            _ = apify_client.user().get()
        except Exception as e:
            raise UserException("Failed to get user information with the provided Apify API Token. Make sure the token is set correctly: %s" % e)

        actor_run = actor_client.call(run_input = run_input, wait_secs=0)
        if not actor_run:
            raise UserException('Received empty run response. If the error keeps happening, contact Apify support: support@apify.com')
        run_id = actor_run['id']
        logging.info('Started Google Maps Reviews Scraper run. You can check the progress at https://console.apify.com/view/runs/%s' % run_id)

        run_client = apify_client.run(run_id)
        run_client.wait_for_finish()

        dataset_client = apify_client.dataset(actor_run['defaultDatasetId'])
        reviews = dataset_client.list_items().items
        logging.info('Run has finished successfully, it scraped %d reviews' % len(reviews))

        self.write_output_table(reviews)


    """
        Reads input csv file and extracts values from 'place_id' or 'place_url' columns.
        This fails if neither of the columns is present.
        If a row doesn't contain `place_id` nor `place_url`, it will be skipped.
    """
    def read_input_table(self):
        input_tables = self.get_input_tables_definitions()
        if len(input_tables) == 0:
            raise UserException("No input table input was provided. Make sure you have added at least one table input in your configuration (Table Input Mapping).")

        place_ids = []
        start_urls = []

        for input_table in input_tables:
            logging.info(f'Processing input table: {input_table.name} with path: {input_table.full_path}')

            with open(input_table.full_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                columns = list(csv_reader.fieldnames or [])

                if 'place_id' not in columns and 'place_url' not in columns:
                    raise UserException('Expects the input input to contain "place_id" or "place_url columns')

                for row in csv_reader:
                    if (place_id := row.get('place_id')):
                        place_ids.append(place_id)
                    elif (place_url := row.get('place_url')):
                        start_urls.append({ 'url': place_url })

        if len(place_ids) == 0 and len(start_urls) == 0:
            raise Exception('Didn\'t find any place IDs nor URLs. Make sure your input tables have populated "place_id" or "place_url" columns')

        return place_ids, start_urls


    def write_output_table(self, reviews):
        output_table = self.create_out_table_definition('output.csv', incremental=True)
        for col in OUTPUT_COLUMNS:
            output_table.add_column(col)
        self.write_manifest(output_table)

        with open(output_table.full_path, 'w') as file:
            csv_writer = csv.DictWriter(file, OUTPUT_COLUMNS)
            rows = []
            for review in reviews:
                row = {}
                for col in OUTPUT_COLUMNS:
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
