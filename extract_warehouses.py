import time

from sgqlc.operation import Operation

from config.shiphero_schema import shiphero_schema
from utils.common import get_grapql_endpoint, save_json_file


def extract_warehouses():
    """GraphQL Data Extractor"""
    graphql = get_grapql_endpoint()
    op = Operation(shiphero_schema.Query)
    query = op.account()
    query.complexity()
    select = query.data().warehouses()
    select.id()
    select.legacy_id()
    select.identifier()
    select.profile()
    select.company_alias()
    select.address.name()
    select.address.address1()
    select.address.address2()
    select.address.city()
    select.address.country()
    return graphql(op)


start = time.time()
print('Extracting warehouses...')

COMPLEXITY = 0
COST = 0
warehouses = []

try:
    response = extract_warehouses()
    if "errors" in response:
        print(response['errors'][0]['message'])
    data = response['data']['account']
    for warehouse in data['data']['warehouses']:
        warehouse_address = warehouse['address']
        warehouse['name'] = warehouse_address['name']
        warehouse['address1'] = warehouse_address['address1']
        warehouse['address2'] = warehouse_address['address2']
        warehouse['city'] = warehouse_address['city']
        warehouse['country'] = warehouse_address['country']
        del warehouse['address']
        warehouses.append(warehouse)

    COMPLEXITY += data['complexity']
    COST += response['extensions']['throttling']['cost']
except Exception as e:
    print(f"Failed to extract data | Error: {str(e)}")

print(f'Warehouses count: {len(warehouses)}')
print(f'Complexity/cost: {COMPLEXITY}/{COST}')

if warehouses:
    print("Saving warehouses to file...")
    file = save_json_file('warehouses', warehouses)
    print(f"data saved to file: {file}")

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
