import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.order import Order
from models.order_history import OrderHistory
from utils.datetime_parser import from_iso
from utils.common import update_db_record_from_dict, get_json_file_content


def transform_order(order: dict):
    """Transform raw order"""
    if "order_date" in order:
        order["order_date"] = from_iso(order["order_date"])
    if "updated_at" in order:
        order["updated_at"] = from_iso(order["updated_at"])
    if "required_ship_date" in order and order['required_ship_date']:
        order['required_ship_date'] = from_iso(order['required_ship_date'])
    return order


def transform_order_history(history: dict):
    """Transform raw order history"""
    if "created_at" in history:
        history['created_at'] = from_iso(history['created_at'])
    return history


def add_or_update_order(order: dict, existing_orders: list):
    """Create a new order or update an existing order"""
    order = transform_order(order)
    new_record = False
    if order['id'] in existing_orders:
        db_order = existing_orders[order['id']]
    else:
        new_record = True
        db_order = Order()
    db_order = update_db_record_from_dict(db_order, order)
    if new_record:
        return db_order


def add_or_update_order_history(history: dict, existing_histories: list):
    """Create a new order history or update an existing history"""
    history = transform_order_history(history)
    new_record = False
    if history['id'] in existing_histories:
        db_history = existing_histories[history['id']]
    else:
        new_record = True
        db_history = OrderHistory()
    db_history = update_db_record_from_dict(db_history, history)
    if new_record:
        return db_history


def save_to_db(orders: list):
    """Save orders in database"""
    if len(orders) == 0:
        return
    db: Session = session()
    try:
        # Fetching existing records from database
        print("Retrieving existing orders...")
        order_ids = []
        history_ids = []
        for order in orders:
            order_ids.append(order['id'])
            for history in order['order_history']:
                history_ids.append(history['id'])
        existing_orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
        existing_histories = db.query(OrderHistory).filter(
            OrderHistory.id.in_(history_ids)).all()
        existing_orders = {order.id: order for order in existing_orders}
        existing_histories = {history.id: history
                              for history in existing_histories}

        # Updating/Creating new orders
        print(f"Saving {len(orders)} orders...")
        new_items = []
        new_orders = 0
        new_histories = 0
        total_histories = 0
        for order in orders:
            order_history = order["order_history"]
            del order['order_history']
            total_histories += len(order_history)
            new_order = add_or_update_order(order, existing_orders)
            if new_order:
                new_orders += 1
                new_items.append(new_order)
            for history in order_history:
                new_history = add_or_update_order_history(history,
                                                          existing_histories)
                if new_history:
                    new_histories += 1
                    new_items.append(new_history)
        if new_items:  # Saving new orders
            print('Saving new records...')
            db.add_all(new_items)
        print('Commiting changes to database...')
        db.commit()
        print('Orders saved!')
        print(f'New orders: {new_orders} | New histories: {new_histories} | Existing orders: {len(orders)-new_orders} | Existing histories: {total_histories-new_histories}')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
init_db()
orders_raw = get_json_file_content("data/orders")
save_to_db(orders_raw)
print(f'Time taken: {time.time()-start} sec')
