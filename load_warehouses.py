import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.warehouse import Warehouse
from utils.common import get_json_file_content, transform_data
from utils.db import db_upsert


def transform_warehouse(warehouse: dict):
    """Transform raw warehouse"""
    if "company_alias" in warehouse and not warehouse['company_alias']:
        warehouse['company_alias'] = None
    if "address2" in warehouse and not warehouse['address2']:
        warehouse['address2'] = None
    return warehouse


def save_to_db(warehouses: list):
    """Save warehouses in database"""
    if len(warehouses) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(warehouses)} warehouses...")
        db_upsert(db, Warehouse, warehouses)
        print('Commiting changes to database...')
        db.commit()
        print('Warehouses saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
print('Connecting to database...')
init_db()
print('Retrieving raw data...')
warehouses_raw = get_json_file_content("data/warehouses/2024/9/10/1")
print(f"Transforming {len(warehouses_raw)} warehouses...")
warehouses_transformed = transform_data(warehouses_raw, transform_warehouse)
save_to_db(warehouses_transformed)
print(f'Time taken: {time.time()-start} sec')
