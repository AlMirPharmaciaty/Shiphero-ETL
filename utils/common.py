import os
import json
from datetime import datetime

from sgqlc.endpoint.http import HTTPEndpoint
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.mysql import insert as mysql_insert
from config.settings import DB_URL

from config.settings import AUTH_TOKEN


def get_grapql_endpoint():
    """returns Shiphero graphql http endpoint with auth in header"""
    return HTTPEndpoint('https://public-api.shiphero.com/graphql',
                        base_headers={'Authorization': f'Bearer {AUTH_TOKEN}'})


def update_db_record_from_dict(db_record, data: dict):
    """Set db item value from dict"""
    for key, value in data.items():
        if hasattr(db_record, key):
            setattr(db_record, key, value)
    return db_record


def get_json_file_content(filename: str):
    """load json file content"""
    data = []
    with open(f'{filename}.jsonl', "r", encoding="utf-8") as file:
        for obj in file:
            obj = json.loads(obj)
            data.append(obj)
    return data


def save_json_file(folder: str, content: list):
    """save content to a json file"""
    today = datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    directory_path = os.path.join('data', folder, year, month, day)
    os.makedirs(directory_path, exist_ok=True)
    files = os.listdir(directory_path)
    filename = os.path.join(directory_path, f"{len(files) + 1}.jsonl")
    with open(filename, "w", encoding="utf-8") as file:
        for entry in content:
            json.dump(entry, file)
            file.write('\n')
    return filename


def transform_data(raw_data: list, transform_func):
    """Transform a collection of raw data"""
    for index, data in enumerate(raw_data):
        raw_data[index] = transform_func(data)
    return raw_data


def db_upsert(db: Session, model, data: list, batch_size: int = 1500):
    """Upsert data into database"""
    table = model.__table__
    primary_keys = [key.name for key in inspect(table).primary_key]
    for i in range(0, len(data), batch_size):
        if DB_URL.startswith("mysql"):
            stmt = mysql_insert(table).values(data[i:i+batch_size])
            stmt = stmt.on_duplicate_key_update(stmt.inserted)
        else:
            stmt = sqlite_insert(table).values(data[i:i+batch_size])
            stmt = stmt.on_conflict_do_update(index_elements=primary_keys,
                                              set_=stmt.excluded)
        db.execute(stmt)
