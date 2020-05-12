import logging
import pytest
import json
from json_tools.encoder import SimpleJSONEncoder

logger = logging.getLogger(__name__)

def test_custom_class(person):
    jstr = json.dumps(person, cls=SimpleJSONEncoder)
    logger.debug(jstr)
    assert jstr == r'{"name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}'

def test_custom_class_with_none_fields(person_with_none_fields):
    jstr = json.dumps(person_with_none_fields, cls=SimpleJSONEncoder)
    logger.info(jstr)
    assert 'null' not in jstr
    SimpleJSONEncoder.skip_none_fields = False
    jstr = json.dumps(person_with_none_fields, cls=SimpleJSONEncoder)
    logger.info(jstr)
    assert 'null' in jstr