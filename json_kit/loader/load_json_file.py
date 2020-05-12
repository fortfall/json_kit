import os
import json
from chardet import detect
from .utils import is_pathname_valid

def detect_encoding(filename):
    with open(filename, 'rb') as fp:
        rawdata = fp.read()
        try:
            return detect(rawdata)['encoding']
        except:
            return None

def load_json_file(filename: str) -> object:
    if not is_pathname_valid(filename):
        raise Exception(f"Invalid filename: {filename}")
    elif not os.path.exists(filename):
        raise Exception(f"{filename} not exists.")
    try:
        with open(filename, 'utf-8') as fp:
            return json.load(fp)
    except UnicodeDecodeError as e:
        detected_encoding = detected_encoding(filename)
        if detected_encoding is None:
            raise Exception(f"Unable to load {filename}.\n Error: {str(e)}")
        else:
            with open(filename, 'r', encoding=detected_encoding) as fp:
                return json.load(fp)
