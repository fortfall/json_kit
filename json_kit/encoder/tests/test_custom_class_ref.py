import logging
import pytest
import json
from json_kit.encoder import RefJSONEncoder

logger = logging.getLogger(__name__)

def test_person_list(person_list):
    jstr = json.dumps(person_list, cls=RefJSONEncoder)
    logger.debug(jstr)
    assert jstr == r'[{"$id": "1", "name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}, {"$ref": "1"}]'

