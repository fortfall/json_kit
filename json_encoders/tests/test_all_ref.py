import logging
import pytest
import json
from json_encoders import AllRefJSONEncoder

logger = logging.getLogger(__name__)

def test_persons_with_same_hobbies(persons_with_same_hobbies):
    jstr = json.dumps(persons_with_same_hobbies, cls=AllRefJSONEncoder)
    logger.debug(jstr)
    assert jstr == r'[{"$id": "1", "$values": {"name": "Jack", "age": 33, "job": 0, "hobbies": {"$id": "2", "$values": ["Swimming", "Video Games", "Fishing"]}}}, {"$ref": "1"}, {"name": "Mike", "age": 24, "job": 2, "hobbies": {"$ref": "2"}}]'
