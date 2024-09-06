import json


def update_db_record_from_dict(db_record, data: dict):
    """Set db item value from dict"""
    for key, value in data.items():
        if hasattr(db_record, key):
            setattr(db_record, key, value)
    return db_record


def get_json_file_content(file_path: str):
    """load json file content"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
