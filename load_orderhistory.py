import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.order_history import OrderHistory
from utils.datetime_parser import from_iso
from utils.common import get_json_file_content, transform_data, db_upsert


def transform_order_history(history: dict):
    """Transform raw order history"""
    if "created_at" in history:
        history['created_at'] = from_iso(history['created_at'])
    return history


def save_to_db(order_histories: list):
    """Save orders in database"""
    if len(order_histories) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(order_histories)} order histories...")
        db_upsert(db, OrderHistory, order_histories)
        print('Commiting changes to database...')
        db.commit()
        print('Order histories saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
init_db()
order_history_raw = get_json_file_content("data/order_history/2024/9/9/1")
print(f"Transforming {len(order_history_raw)} order histories...")
order_history_transformed = transform_data(order_history_raw,
                                           transform_order_history)
save_to_db(order_history_transformed)
print(f'Time taken: {time.time()-start} sec')
