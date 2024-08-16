import json
import time
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint
from schema import schema

start = time.time()
print('Extracting orders...')

with open('token.txt', 'r', encoding='utf-8') as f:
    AUTH_TOKEN = f.read()

graphql = HTTPEndpoint('https://public-api.shiphero.com/graphql',
                       base_headers={'Authorization': f'Bearer {AUTH_TOKEN}'})


def extract_data(from_date, limit=10, after=''):
    """
    GraphQL Data Extractor
    """
    # Build the query
    op = Operation(schema.Query)
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
orders = []

while GO_TO_NEXT_PAGE:
    print(f"Extracting page: {str(PAGE_COUNT+1)}           ", end='\r')
    try:
        data = extract_data(from_date='2024-05-01',
                            limit=100,
                            after=NEXT_PAGE)['data']['orders']
        for order in data['data']['edges']:
            orders.append(order['node'])
        TOTAL_COMPLEXITY += data['complexity']
        page_info = data['data']['pageInfo']
        GO_TO_NEXT_PAGE = page_info['hasNextPage']
        NEXT_PAGE = page_info['endCursor']
        PAGE_COUNT += 1
    except Exception as e:
        print("Failed to extract data... retrying in 10s --- Error:", e)
    if GO_TO_NEXT_PAGE:
        # ======================================================
        # Replace the below for loop with time.sleep(10) in prod
        # and remove end param and whitespaces from print funcs
        # ======================================================
        wait = 10
        for i in range(wait):
            count = f"{'0' if (wait-i)<wait else ''}{wait - i}"
            print(f"Page {PAGE_COUNT} extracted. Waiting {count}s", end='\r')
            time.sleep(1)

print(f'Orders count: {len(orders)}     ')
print(f'Total complexity: {TOTAL_COMPLEXITY} ({PAGE_COUNT} requests)')

with open("orders.json", "w", encoding="utf-8") as file:
    json.dump(orders, file)

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
