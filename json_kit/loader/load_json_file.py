import os
import json
from pathlib import Path
from typing import Union
from chardet import detect

def detect_encoding(filename):
    with open(filename, 'rb') as fp:
        rawdata = fp.read()
        try:
            return detect(rawdata)['encoding']
        except:
            return None

def load_json_file(filename: Union[str, Path]) -> object:
    try:
        with open(filename, 'r', encoding='utf-8') as fp:
            return json.load(fp)
    except UnicodeDecodeError as e:
        encoding = detect_encoding(filename)
        if encoding is None:
            raise Exception(f"Unable to load {filename}.\n Error: {str(e)}")
        else:
            with open(filename, 'r', encoding=encoding) as fp:
                return json.load(fp)
