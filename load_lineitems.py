import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.line_item import LineItem
from utils.common import update_db_record_from_dict, get_json_file_content


def add_or_update_line_item(line_item: dict, existing_line_items: list):
    """Create a new line_item or update an existing line item"""
    new_record = False
    if line_item['id'] in existing_line_items:
        db_line_item = existing_line_items[line_item['id']]
    else:
        new_record = True
        db_line_item = LineItem()
    db_line_item = update_db_record_from_dict(db_line_item, line_item)
    if new_record:
        return db_line_item


def save_to_db(line_items: list):
    """Save line items in database"""
    if len(line_items) == 0:
        return
    db: Session = session()
    try:
        # Fetching existing records from database
        print("Retrieving existing line items...")
        line_item_ids = [line_item['id'] for line_item in line_items]
        existing_line_items = db.query(LineItem).filter(
            LineItem.id.in_(line_item_ids)).all()
        existing_line_items = {
            line_item.id: line_item for line_item in existing_line_items}

        # Updating/Creating new orders
        print(f"Saving {len(line_items)} line items...")
        new_items = []
        for line_item in line_items:
            new_line_item = add_or_update_line_item(
                line_item, existing_line_items)
            if new_line_item:
                new_items.append(new_line_item)
        if new_items:  # Saving new line_items
            print('Saving new records...')
            db.add_all(new_items)
        print('Commiting changes to database...')
        db.commit()
        print('Line items saved!')
        print(
            f'New line items: {len(new_items)} | Existing line items: {len(line_items)-len(new_items)}')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
init_db()
line_items_raw = get_json_file_content("data/line_items")
save_to_db(line_items_raw)
print(f'Time taken: {time.time()-start} sec')
