import time
import json
from datetime import datetime
import csv

start = time.time()
print('Transforming orders...')


with open("data/orders.json", "r", encoding="utf-8") as file:
    orders = json.load(file)


orders_transformed = []
TOTAL_FULFILLMENT_DIFF = 0

for order in orders:
    data = {}
    data['id'] = order['id']
    data['order_number'] = order['order_number']
    data['partner_order_id'] = order['partner_order_id']
    data['status'] = order['fulfillment_status']
    data['source'] = order['source']
    data['shop_name'] = order['shop_name']
    data['total_price'] = order['total_price']
    data['created_at'] = ''
    data['shipped_at'] = ''
    data['created_by'] = ''
    data['shipped_by'] = ''
    data['fulfillment_time'] = ''
    data['fulfillment_time_secs'] = ''

    # Get order creation and shipping details from history
    for history in order['order_history']:
        if "created" in history['information'].lower():
            data['created_at'] = datetime.fromisoformat(history['created_at'])
            data['created_by'] = history['username']
        if 'shipped' in history['information'].lower():
            data['shipped_at'] = datetime.fromisoformat(history['created_at'])
            data['shipped_by'] = history['username']

    # calculate time taken to fulfil the order
    if data['created_at'] and data['shipped_at']:
        diff = data['shipped_at'] - data['created_at']
        data['fulfillment_time_secs'] = diff.total_seconds()
        TOTAL_FULFILLMENT_DIFF += diff.total_seconds()
        diff = f"{diff.days} days {diff.seconds // 3600} hrs {(diff.seconds % 3600) // 60} mins"
        data['fulfillment_time'] = diff
    orders_transformed.append(data)

# Calculate average time of orders fulfillment
avg_time = TOTAL_FULFILLMENT_DIFF/len(orders)
days, remainder = divmod(avg_time, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, _ = divmod(remainder, 60)
print(f"""Average order fulfillment time:
      {int(days)} days {int(hours)} hrs {int(minutes)} mins""")


with open('data/orders.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.DictWriter(file,
                                fieldnames=list(orders_transformed[0].keys()))
    csv_writer.writeheader()
    csv_writer.writerows(orders_transformed)

print(f'Extraction completed --- time taken: {(time.time()-start)} sec')
