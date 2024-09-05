import json
import time
import argparse
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from config.settings import AUTH_TOKEN
from config.shiphero_schema import shiphero_schema
from utils.datetime_parser import to_iso

FILTER_FROM_DATE = "2024-08-01"
FILTER_LIMIT = 100
REQUEST_INTERVAL = 10

start = time.time()
print('Extracting orders...')


parser = argparse.ArgumentParser()
parser.add_argument("--date", help="From date filter")
parser.add_argument("--limit", help="Number of orders extracted per request")
parser.add_argument("--interval", help="Seconds to wait before each request")
args = parser.parse_args()
if args.date:
    FILTER_FROM_DATE = str(args.date)
if args.limit:
    FILTER_LIMIT = int(args.limit)
if args.interval:
    REQUEST_INTERVAL = int(args.interval)


graphql = HTTPEndpoint('https://public-api.shiphero.com/graphql',
                       base_headers={'Authorization': f'Bearer {AUTH_TOKEN}'})


def extract_orders(from_date, limit=10, after=''):
    """
    GraphQL Data Extractor
    """
    # Build the query
    op = Operation(shiphero_schema.Query)
    # Building the orders query
    query = op.orders(order_date_from=from_date)
    # Make sure to request the complexity and request_id
    query.complexity()
    query.request_id()
    # Get the first N data and define the selections
    query_data = query.data(first=limit, after=after)
    select = query_data.edges.node
    select.id()
    select.order_number()
    select.partner_order_id()
    select.fulfillment_status()
    select.source()
    select.shop_name()
    select.total_price()
    select.tags()
    select.order_history.id()
    select.order_history.information()
    select.order_history.created_at()
    select.order_history.username()
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
                              limit=FILTER_LIMIT,
                              after=NEXT_PAGE)['data']['orders']
        for order in data['data']['edges']:
            order = order['node']
            order['extracted_at'] = to_iso()
            orders.append(order)
        TOTAL_COMPLEXITY += data['complexity']
        page_info = data['data']['pageInfo']
        GO_TO_NEXT_PAGE = page_info['hasNextPage']
        NEXT_PAGE = page_info['endCursor']
        PAGE_COUNT += 1
    except Exception as e:
        FAILS += 1
        if REQUEST_INTERVAL > 30:
            REQUEST_INTERVAL += 5
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
print(f'Total complexity: {TOTAL_COMPLEXITY} ({PAGE_COUNT} requests/{FAILS} fails)')

with open("data/orders.json", "w", encoding="utf-8") as file:
    json.dump(orders, file)

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
