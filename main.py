from keboola.component import CommonInterface
import csv
import logging
from apify_client import ApifyClient

ci = CommonInterface(data_folder_path='./data')

logging.info(ci.environment_variables.project_id)

token = ci.configuration.parameters['#token']

run_input = {
    'language': ci.configuration.parameters['language'],
    'maxReviews': ci.configuration.parameters['maxReviews'],
    'personalData': ci.configuration.parameters['personalData'],
    'reviewsOrigin': ci.configuration.parameters['reviewsOrigin'],
    'reviewsSort': ci.configuration.parameters['reviewsSort'],
}

reviews_start_date = ci.configuration.parameters['reviewsStartDate']
if reviews_start_date:
    run_input['reviewsStartDate'] = reviews_start_date


memory = ci.configuration.parameters['memory']
timeout = ci.configuration.parameters['timeout']

logging.info(run_input)

input_tables = ci.configuration.tables_input_mapping # ci.get_input_tables_definitions()
# print(input_tables )
# ci.get_input_tables_definitions()
place_ids = []
start_urls = []

for table in input_tables:
    print(table.destination)
    with open(table.full_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        print(csv_reader.fieldnames)
        for row in csv_reader:
            if row['place_id']:
                place_ids.append(row['place_id'])
            elif row['place_url']:
                start_urls.append({ 'url': row['place_url'] })

print('place_ids', place_ids)
print('start_urls', start_urls)

run_input['placeIds'] = place_ids
run_input['startUrls'] = start_urls

# apify_client = ApifyClient(token)
# actor_client = apify_client.actor('Xb8osYTtOjlsgI6k9')
# actor_run = actor_client.call(run_input = run_input, memory_mbytes=memory, timeout_secs=timeout)
# if not actor_run:
#     raise Exception('Received empty run response')

# dataset_id = actor_run['defaultDatasetId']
# dataset_client = apify_client.dataset(dataset_id)
# items = dataset_client.list_items()
# print(items.items[0])

out = {'searchString': 'Direct Detail URL: https://www.google.com/maps/search/?api=1&query=The%20Lakeside%20Hotel%20and%20Leisure%20Centre&query_place_id=ChIJkR671oyeXEgR_w6SsjWTeiQ', 'reviewerId': '118196647845804662115', 'reviewerUrl': 'https://www.google.com/maps/contrib/118196647845804662115?hl=en', 'name': 'Seán Moroney', 'reviewerNumberOfReviews': 2, 'isLocalGuide': False, 'reviewerPhotoUrl': 'https://lh3.googleusercontent.com/a-/ALV-UjVtPXeR6gHg2yphpfJBnZDxusQvQjNcghfyRXyDRq7xrNkMzdfc=s1920-c-rp-mo-br100', 'text': 'I have just left and it was the most delightful experience ive had at a bar in quite a while. Thanks to the lovely bartenders, Liam and Oisin who really made the evening for me and my partner. Will be back again especially if these gentlemen are there', 'textTranslated': None, 'publishAt': 'a day ago', 'publishedAtDate': '2025-03-23T00:13:18.727Z', 'likesCount': 0, 'reviewId': 'ChdDSUhNMG9nS0VJQ0FnTUR3OEozbDNRRRAB', 'reviewUrl': 'https://www.google.com/maps/reviews/data=!4m8!14m7!1m6!2m5!1sChdDSUhNMG9nS0VJQ0FnTUR3OEozbDNRRRAB!2m1!1s0x0:0x247a9335b2920eff!3m1!1s2@1:CIHM0ogKEICAgMDw8J3l3QE%7CCgwInqT9vgYQgOLg2gI%7C?hl=en', 'reviewOrigin': 'Google', 'stars': 5, 'rating': None, 'responseFromOwnerDate': None, 'responseFromOwnerText': None, 'reviewImageUrls': [], 'reviewContext': {}, 'reviewDetailedRating': {'Service': 5, 'Location': 4}, 'visitedIn': None, 'originalLanguage': 'en', 'translatedLanguage': None, 'isAdvertisement': False, 'placeId': 'ChIJkR671oyeXEgR_w6SsjWTeiQ', 'location': {'lat': 52.811047, 'lng': -8.444048}, 'address': 'Cullenagh, Killaloe, Co. Clare, V94 E2D6, Ireland', 'neighborhood': 'Cullenagh', 'street': None, 'city': 'Killaloe', 'postalCode': 'V94 E2D6', 'state': 'Co. Clare', 'countryCode': 'IE', 'categoryName': 'Hotel', 'categories': ['Hotel', 'Bar', 'Conference center', 'Gym', 'Restaurant', 'Swimming pool', 'Wedding venue'], 'title': 'The Lakeside Hotel and Leisure Centre', 'totalScore': 4.5, 'permanentlyClosed': False, 'temporarilyClosed': False, 'reviewsCount': 1568, 'url': 'https://www.google.com/maps/search/?api=1&query=The%20Lakeside%20Hotel%20and%20Leisure%20Centre&query_place_id=ChIJkR671oyeXEgR_w6SsjWTeiQ', 'price': None, 'cid': '2628575191362572031', 'fid': '0x485c9e8cd6bb1e91:0x247a9335b2920eff', 'hotelStars': '4-star hotel', 'imageUrl': 'https://photos.hotelbeds.com/giata/original/28/283500/283500a_hb_a_042.jpg', 'scrapedAt': '2025-03-24T19:17:22.980Z', 'language': 'en'}
result_table = ci.create_out_table_definition('output')
with open(result_table.full_path, 'w') as file:
    csv_writer = csv.DictWriter(file, ['placeId', 'reviewId', 'reviewerId'])
    csv_writer.writerows([{
        'placeId': out['placeId'],
        'reviewId': out['reviewId'],
        'reviewerId': out['reviewerId'],
    }])

    # print(t.full_path)
    # table_def = ci.get_input_table_definition_by_name(t.destination)
    # print(table_def.name)
    
    # print(t.column_types[0][1])
    # logging.info(ci.get_input_table_definition_by_name(t.destination).__dict__)

