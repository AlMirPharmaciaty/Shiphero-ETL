import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.shipment import Shipment
from utils.datetime_parser import from_iso
from utils.common import get_json_file_content, transform_data, db_upsert


def transform_shipment(shipment: dict):
    """Transform raw shipment object"""
    if "created_date" in shipment:
        shipment["created_date"] = from_iso(shipment["created_date"])
    return shipment


def save_to_db(shipments: list):
    """Save shipments in database"""
    if len(shipments) == 0:
        return
    db: Session = session()
    try:
        print(f"Saving {len(shipments)} shipments...")
        db_upsert(db, Shipment, shipments)
        print('Commiting changes to database...')
        db.commit()
        print('Shipments saved!')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
init_db()
shipments_raw = get_json_file_content("data/shipments")
print(f"Transforming {len(shipments_raw)} shipments...")
shipments_transformed = transform_data(shipments_raw, transform_shipment)
save_to_db(shipments_raw)
print(f'Time taken: {time.time()-start} sec')
