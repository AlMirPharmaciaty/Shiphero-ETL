import os
import json
from datetime import datetime

from sgqlc.endpoint.http import HTTPEndpoint

from config.settings import AUTH_TOKEN


def get_grapql_endpoint():
    """returns Shiphero graphql http endpoint with auth in header"""
    return HTTPEndpoint('https://public-api.shiphero.com/graphql',
                        base_headers={'Authorization': f'Bearer {AUTH_TOKEN}'})


def update_one_dict_from_another(dict_one, dict_two):
    """Set db item value from dict"""
    for key, value in dict_two.items():
        if hasattr(dict_one, key):
            setattr(dict_one, key, value)
    return dict_one


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

    last_file = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".jsonl"):
            number = int(filename.split(".")[0])
            last_file = max(last_file, number)

    filename = os.path.join(directory_path, f"{last_file + 1}.jsonl")
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
