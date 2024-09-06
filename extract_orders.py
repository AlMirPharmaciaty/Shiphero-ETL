import json
import time
import argparse
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from config.settings import AUTH_TOKEN
from config.shiphero_schema import shiphero_schema

FILTER_FROM_DATE = "2024-08-01"
FILTER_DATE_TO = None
FILTER_LIMIT = 100
REQUEST_INTERVAL = 10

start = time.time()
print('Extracting orders...')

parser = argparse.ArgumentParser()
parser.add_argument("--datefrom", help="From date filter")
parser.add_argument("--dateto", help="To date filter")
parser.add_argument("--limit", help="Number of orders extracted per request")
parser.add_argument("--interval", help="Seconds to wait before each request")
args = parser.parse_args()
if args.datefrom:
    FILTER_FROM_DATE = str(args.datefrom)
if args.dateto:
    FILTER_DATE_TO = str(args.dateto)
if args.limit:
    FILTER_LIMIT = int(args.limit)
if args.interval:
    REQUEST_INTERVAL = int(args.interval)


graphql = HTTPEndpoint('https://public-api.shiphero.com/graphql',
                       base_headers={'Authorization': f'Bearer {AUTH_TOKEN}'})


def extract_orders(from_date, date_to=None, limit=10, after=''):
    """
    GraphQL Data Extractor
    """
    # Build the query
    op = Operation(shiphero_schema.Query)
    # Building the orders query
    if date_to:
        query = op.orders(order_date_from=from_date, order_date_to=date_to)
    else:
        query = op.orders(order_date_from=from_date)
    # Make sure to request the complexity and request_id
    query.complexity()
    query.request_id()
    # Get the first N data and define the selections
    query_data = query.data(first=limit, after=after)
    select = query_data.edges.node
    select.id()
    select.legacy_id()
    select.order_number()
    select.shop_name()
    select.fulfillment_status()
    select.order_date()
    select.total_tax()
    select.subtotal()
    select.total_discounts()
    select.total_price()
    select.ready_to_ship()
    select.email()
    select.profile()
    select.required_ship_date()
    select.tags()
    select.flagged()
    select.source()
    select.allow_partial()
    select.updated_at()
    select.order_history.id()
    select.order_history.legacy_id()
    select.order_history.order_id()
    select.order_history.user_id()
    select.order_history.account_id()
    select.order_history.username()
    select.order_history.order_number()
    select.order_history.information()
    select.order_history.created_at()
    # Pagination info
    query_data.page_info.has_next_page()
    query_data.page_info.end_cursor()
    # Executing the call
    return graphql(op)


GO_TO_NEXT_PAGE = True
PAGE_COUNT = 0
NEXT_PAGE = ''
TOTAL_COMPLEXITY = 0
FAILS = 0
orders = []

while GO_TO_NEXT_PAGE:
    print(f"Extracting page: {str(PAGE_COUNT+1)}           ", end='\r')
    try:
        data = extract_orders(from_date=FILTER_FROM_DATE,
                              date_to=FILTER_DATE_TO,
                              limit=FILTER_LIMIT,
                              after=NEXT_PAGE)
        # if "errors" in data:
        #     print(data['errors'][0]['message'])
        data = data['data']['orders']
        for order in data['data']['edges']:
            orders.append(order['node'])
        TOTAL_COMPLEXITY += data['complexity']
        page_info = data['data']['pageInfo']
        GO_TO_NEXT_PAGE = page_info['hasNextPage']
        NEXT_PAGE = page_info['endCursor']
        PAGE_COUNT += 1
    except Exception as e:
        FAILS += 1
        print(
            f"Failed to extract data | Retrying in {REQUEST_INTERVAL}s | Error: {str(e)}")
    if GO_TO_NEXT_PAGE:
        # ======================================================
        # Replace the below for loop with time.sleep(REQUEST_INTERVAL) in prod
        # and remove end param and whitespaces from print funcs
        # ======================================================
        for i in range(REQUEST_INTERVAL):
            count = f"{'0' if (REQUEST_INTERVAL-i)<REQUEST_INTERVAL else ''}{REQUEST_INTERVAL - i}"
            print(f"Page {PAGE_COUNT} extracted. Waiting {count}s", end='\r')
            time.sleep(1)

print(f'Orders count: {len(orders)}     ')
print(
    f'Total complexity: {TOTAL_COMPLEXITY} ({PAGE_COUNT} requests/{FAILS} fails)')

with open("data/orders.json", "w", encoding="utf-8") as file:
    json.dump(orders, file)

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
