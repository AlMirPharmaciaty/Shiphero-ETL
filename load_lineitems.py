import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.line_item import LineItem
from utils.common import get_json_file_content
from utils.db import db_upsert


def save_to_db(line_items: list):
    """Save line items in database"""
    if len(line_items) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(line_items)} line items...")
        db_upsert(db, LineItem, line_items)
        print('Commiting changes to database...')
        db.commit()
        print('Line items saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
print('Connecting to database...')
init_db()
print('Retrieving raw data...')
line_items_raw = get_json_file_content("data/line_items/2024/9/10/1")
save_to_db(line_items_raw)
print(f'Time taken: {time.time()-start} sec')
