import logging
import pytest
import json
from json_encoders import SimpleJSONEncoder

logger = logging.getLogger(__name__)

def test_custom_class(person):
    jstr = json.dumps(person, cls=SimpleJSONEncoder)
    logger.debug(jstr)
    assert jstr == r'{"name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}'
