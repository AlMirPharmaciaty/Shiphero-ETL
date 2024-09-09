import time
import argparse

from sgqlc.operation import Operation

from config.shiphero_schema import shiphero_schema
from utils.common import get_grapql_endpoint, save_json_file

FILTERS = {
    "date_from": None,
    "date_to": None,
}
REQUEST_LIMIT = 100
REQUEST_INTERVAL = 10

parser = argparse.ArgumentParser()
parser.add_argument("--datefrom", help="From date filter")
parser.add_argument("--dateto", help="To date filter")
parser.add_argument("--limit", help="Number of orders extracted per request")
parser.add_argument("--interval", help="Seconds to wait before each request")
args = parser.parse_args()
if args.datefrom:
    FILTERS['date_from'] = str(args.datefrom)
if args.dateto:
    FILTERS['date_to'] = str(args.dateto)
if args.limit:
    REQUEST_LIMIT = int(args.limit)
if args.interval:
    REQUEST_INTERVAL = int(args.interval)

FILTERS = {key: value for key, value in FILTERS.items() if value}


def extract_packsperday(filters: dict, limit: int = 10, after: str = ''):
    """GraphQL Data Extractor"""
    graphql = get_grapql_endpoint()
    op = Operation(shiphero_schema.Query)
    # Building the orders query
    query = op.packs_per_day(**filters)
    # Make sure to request the complexity and request_id
    query.complexity()
    query.request_id()
    # Get the first N data and define the selections
    query_data = query.data(first=limit, after=after)
    select = query_data.edges.node
    select.id()
    select.legacy_id()
    select.order_id()
    select.warehouse_id()
    select.shipment_id()
    select.user_id()
    select.user_first_name()
    select.user_last_name()
    select.created_at()
    # Pagination info
    query_data.page_info.has_next_page()
    query_data.page_info.end_cursor()
    # Executing the call
    return graphql(op)


start = time.time()
print('Extracting packs per day...')

GO_TO_NEXT_PAGE = True
PAGE_COUNT = 0
NEXT_PAGE = ''
TOTAL_COMPLEXITY = 0
TOTAL_COST = 0
FAILS = 0
packs_per_day = []

while GO_TO_NEXT_PAGE:
    print(f"Extracting page: {str(PAGE_COUNT+1)}           ", end='\r')
    try:
        response = extract_packsperday(filters=FILTERS,
                                       limit=REQUEST_LIMIT,
                                       after=NEXT_PAGE)
        # if "errors" in response:
        #     print(response['errors'][0]['message'])
        data = response['data']['packs_per_day']
        for ppd in data['data']['edges']:
            packs_per_day.append(ppd['node'])

        TOTAL_COMPLEXITY += data['complexity']
        TOTAL_COST += response['extensions']['throttling']['cost']
        page_info = data['data']['pageInfo']
        GO_TO_NEXT_PAGE = page_info['hasNextPage']
        NEXT_PAGE = page_info['endCursor']
        PAGE_COUNT += 1
    except Exception as e:
        FAILS += 1
        print(
            f"Failed to extract data ({FAILS}) | Retrying in {REQUEST_INTERVAL}s | Error: {str(e)}")
    if GO_TO_NEXT_PAGE:
        # ======================================================
        # Replace the below for loop with time.sleep(REQUEST_INTERVAL) in prod
        # and remove end param and whitespaces from print funcs
        # ======================================================
        for i in range(REQUEST_INTERVAL):
            count = f"{'0' if (REQUEST_INTERVAL-i)<REQUEST_INTERVAL else ''}{REQUEST_INTERVAL - i}"
            print(f"Page {PAGE_COUNT} extracted. Waiting {count}s", end='\r')
            time.sleep(1)

print(f'Packs per day count: {len(packs_per_day)}')
print(
    f'Total complexity/cost: {TOTAL_COMPLEXITY}/{TOTAL_COST} ({PAGE_COUNT} requests/{FAILS} fails)')

if packs_per_day:
    print("Saving packs per day to file...")
    file = save_json_file('packs_per_day', packs_per_day)
    print(f"data saved to file: {file}")

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
