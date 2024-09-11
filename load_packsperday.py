import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.packs_per_day import PacksPerDay
from utils.datetime_parser import from_iso
from utils.common import get_json_file_content, transform_data
from utils.db import db_upsert

from config.settings import DB_URL


def transform_ppd(ppd: dict):
    """Transform raw pack per day"""
    if "created_at" in ppd:
        ppd["created_at"] = from_iso(ppd["created_at"])
    return ppd


def save_to_db(ppd: list):
    """Save packs per day in database"""
    if len(ppd) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(ppd)} packs per day...")
        db_upsert(db, PacksPerDay, ppd)
        print('Commiting changes to database...')
        db.commit()
        print('Packs per day saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
print('Connecting to database...')
init_db()
print('Retrieving raw data...')
packs_per_day_raw = get_json_file_content("data/packs_per_day/2024/9/11/1")
print(f"Transforming {len(packs_per_day_raw)} packs per day...")
packs_per_day_transformed = transform_data(packs_per_day_raw, transform_ppd)
save_to_db(packs_per_day_transformed)
print(f'Time taken: {time.time()-start} sec')
