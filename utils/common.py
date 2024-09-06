import json

from sgqlc.endpoint.http import HTTPEndpoint

from config.settings import AUTH_TOKEN


def get_grapql_endpoint():
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
    with open(f'{filename}.json', "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(filename: str, content):
    """save content to a json file"""
    with open(f"{filename}.json", "w", encoding="utf-8") as file:
        json.dump(content, file)
