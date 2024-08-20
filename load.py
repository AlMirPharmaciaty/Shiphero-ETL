import csv
import time
from sqlalchemy.orm import Session

from config.database import init_db, session
from models.order import Order
from utils.datetime_parser import from_iso

start = time.time()
print('Loading orders to database...')

orders = []
with open('data/orders.csv', encoding='utf-8') as file:
    orders = list(csv.DictReader(file))

ADDED_COUNT = FAILED_COUNT = EXISTS_COUNT = 0
if orders:
    init_db()
    db: Session = session()
    for order in orders:
        try:
            if db.query(Order).filter(Order.id == order['id']).first():
                EXISTS_COUNT += 1
            else:
                new_order = Order(**order)
                new_order.created_at = from_iso(new_order.created_at)
                if order['shipped_at']:
                    new_order.shipped_at = from_iso(order['shipped_at'])
                    new_order.fulfillment_time_secs = float(
                        order['fulfillment_time_secs'])
                else:
                    new_order.shipped_at = None
                    new_order.shipped_by = None
                    new_order.fulfillment_time = None
                    new_order.fulfillment_time_secs = None
                new_order.total_price = float(new_order.total_price)
                new_order.extracted_at = from_iso(new_order.extracted_at)
                new_order.transformed_at = from_iso(new_order.transformed_at)
                db.add(new_order)
                db.commit()
                ADDED_COUNT += 1
        except Exception as e:
            db.rollback()
            FAILED_COUNT += 1
            print('Failed to add to database:', str(e))
        print(f'Total: {len(orders)} | Added: {ADDED_COUNT} | Failed: {FAILED_COUNT} | Already Exists: {EXISTS_COUNT}',
              end='\r')

print(f'Total: {len(orders)} | Added: {ADDED_COUNT} | Failed: {FAILED_COUNT} | Already Exists: {EXISTS_COUNT}')
print(f'Orders loaded to database --- time taken: {(time.time()-start)} sec')
