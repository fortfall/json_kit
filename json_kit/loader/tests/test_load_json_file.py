import pytest
from json_kit.loader import load_json_file

def test_load_json_file(sample_jsons):
    for f in sample_jsons:
        try:
            obj = load_json_file(f)
            assert obj is not None
        except:
            assert obj is not None