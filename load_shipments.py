import time

from sqlalchemy.orm import Session

from config.database import init_db, session
from models.shipment import Shipment
from utils.datetime_parser import from_iso
from utils.common import update_db_record_from_dict, get_json_file_content


def transform_shipment(shipment: dict):
    """Transform raw shipment object"""
    if "created_date" in shipment:
        shipment["created_date"] = from_iso(shipment["created_date"])
    return shipment


def add_or_update_shipment(shipment: dict, existing_shipments: list):
    """Create a new shipment or update an existing shipment"""
    shipment = transform_shipment(shipment)
    new_record = False
    if shipment['id'] in existing_shipments:
        db_shipment = existing_shipments[shipment['id']]
    else:
        new_record = True
        db_shipment = Shipment()
    db_shipment = update_db_record_from_dict(db_shipment, shipment)
    if new_record:
        return db_shipment


def save_to_db(shipments: list):
    """Save shipments in database"""
    if len(shipments) == 0:
        return
    db: Session = session()
    try:
        # Fetching existing records from database
        print("Retrieving existing shipments...")
        shipment_ids = [shipment['id'] for shipment in shipments]
        existing_shipments = db.query(Shipment).filter(
            Shipment.id.in_(shipment_ids)).all()
        existing_shipments = {
            shipment.id: shipment for shipment in existing_shipments}

        # Updating/Creating new orders
        print(f"Saving {len(shipments)} shipments...")
        new_items = []
        for shipment in shipments:
            new_shipment = add_or_update_shipment(shipment, existing_shipments)
            if new_shipment:
                new_items.append(new_shipment)
        if new_items:  # Saving new shipments
            print('Saving new records...')
            db.add_all(new_items)
        print('Commiting changes to database...')
        db.commit()
        print('Shipments saved!')
        print(
            f'New Shipments: {len(new_items)} | Existing Shipments: {len(shipments)-len(new_items)}')
    except Exception as e:
        db.rollback()
        print(f'Error - {str(e)}')


start = time.time()
init_db()
shipments_raw = get_json_file_content("data/shipments")
save_to_db(shipments_raw)
print(f'Time taken: {time.time()-start} sec')
