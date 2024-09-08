import time
import argparse
from sgqlc.operation import Operation

from config.shiphero_schema import shiphero_schema
from utils.common import get_grapql_endpoint, save_json_file

FILTERS = {
    "order_date_from": None,
    "order_date_to": None,
    "updated_from": None,
    "updated_to": None,
}
REQUEST_LIMIT = 10
REQUEST_INTERVAL = 5

parser = argparse.ArgumentParser()
parser.add_argument("--datefrom", help="From date filter")
parser.add_argument("--dateto", help="To date filter")
parser.add_argument("--updatedfrom", help="Updated from date filter")
parser.add_argument("--updatedto", help="Updated to date filter")
parser.add_argument("--limit", help="Number of orders extracted per request")
parser.add_argument("--interval", help="Seconds to wait before each request")
args = parser.parse_args()
if args.datefrom:
    FILTERS['order_date_from'] = str(args.datefrom)
if args.dateto:
    FILTERS['order_date_to'] = str(args.dateto)
if args.updatedfrom:
    FILTERS['updated_from'] = str(args.updatedfrom)
if args.updatedto:
    FILTERS['updated_to'] = str(args.updatedto)
if args.limit:
    REQUEST_LIMIT = int(args.limit)
if args.interval:
    REQUEST_INTERVAL = int(args.interval)

FILTERS = {key: value for key, value in FILTERS.items() if value}


def extract_lineitems(filters: dict, limit: int = 10, after: str = ''):
    """Shiphero Data Extractor"""
    graphql = get_grapql_endpoint()
    op = Operation(shiphero_schema.Query)
    query = op.orders(**filters)
    query.complexity()

    query_data = query.data(first=limit, after=after)
    select = query_data.edges.node
    select_line_items = select.line_items().edges.node
    select_line_items.id()
    select_line_items.order_id()
    select_line_items.sku()
    select_line_items.quantity()
    select_line_items.product_name()
    select_line_items.price()
    select_line_items.subtotal()
    select_line_items.quantity_allocated()

    query_data.page_info.has_next_page()
    query_data.page_info.end_cursor()
    return graphql(op)


start = time.time()
print('Extracting line items...')


GO_TO_NEXT_PAGE = True
PAGE_COUNT = 0
NEXT_PAGE = ''
TOTAL_COMPLEXITY = 0
TOTAL_COST = 0
FAILS = 0
line_items = []

while GO_TO_NEXT_PAGE:
    print(f"Extracting page: {str(PAGE_COUNT+1)}           ", end='\r')
    try:
        response = extract_lineitems(filters=FILTERS,
                                     limit=REQUEST_LIMIT,
                                     after=NEXT_PAGE)
        if "errors" in response:
            print(response['errors'][0]['message'])
        data = response['data']['orders']
        for order in data['data']['edges']:
            for line_item in order['node']['line_items']['edges']:
                line_items.append(line_item['node'])
        TOTAL_COMPLEXITY += data['complexity']
        TOTAL_COST += response['extensions']['throttling']['cost']
        page_info = data['data']['pageInfo']
        GO_TO_NEXT_PAGE = page_info['hasNextPage']
        NEXT_PAGE = page_info['endCursor']
        PAGE_COUNT += 1
    except Exception as e:
        FAILS += 1
        print(
            f"Failed to extract data | Retrying in {REQUEST_INTERVAL}s | Error: {str(e)}")
    if GO_TO_NEXT_PAGE:
        for i in range(REQUEST_INTERVAL):
            count = f"{'0' if (REQUEST_INTERVAL-i)<REQUEST_INTERVAL else ''}{REQUEST_INTERVAL - i}"
            print(f"Page {PAGE_COUNT} extracted. Waiting {count}s", end='\r')
            time.sleep(1)

print(f'Line items count: {len(line_items)}     ')
print(
    f'Total complexity/cost: {TOTAL_COMPLEXITY}/{TOTAL_COST} ({PAGE_COUNT} requests/{FAILS} fails)')

if line_items:
    print("Saving to file...")
    save_json_file('data/line_items', line_items)
    print("data saved to file!")

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
