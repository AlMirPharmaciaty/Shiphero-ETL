import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.order import Order
from utils.datetime_parser import from_iso
from utils.common import get_json_file_content, transform_data
from utils.db import db_upsert


def transform_order(order: dict):
    """Transform raw order"""
    if "order_date" in order:
        order["order_date"] = from_iso(order["order_date"])
    if "updated_at" in order:
        order["updated_at"] = from_iso(order["updated_at"])
    if "required_ship_date" in order and order['required_ship_date']:
        order['required_ship_date'] = from_iso(order['required_ship_date'])
    return order


def save_to_db(orders: list):
    """Save orders in database"""
    if len(orders) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(orders)} orders...")
        db_upsert(db, Order, orders)
        print('Commiting changes to database...')
        db.commit()
        print('Orders saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
print('Connecting to database...')
init_db()
print('Retrieving raw data...')
orders_raw = get_json_file_content("data/orders/2024/9/9/3")
print(f"Transforming {len(orders_raw)} orders...")
orders_transformed = transform_data(orders_raw, transform_order)
save_to_db(orders_transformed)
print(f'Time taken: {time.time()-start} sec')
