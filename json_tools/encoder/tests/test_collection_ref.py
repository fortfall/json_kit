import logging
import pytest
import json
from json_tools.encoder import AllRefJSONEncoder

logger = logging.getLogger(__name__)

def test_two_identical_list(hobby_list):
    jstr = json.dumps(hobby_list, cls=AllRefJSONEncoder)
    logger.debug(jstr)
    assert jstr == '[{"$id": "1", "$values": ["Swimming", "Video Games", "Fishing"]}, {"$ref": "1"}]'


def test_two_identical_dict(hobby_time_list):
    jstr = json.dumps(hobby_time_list, cls=AllRefJSONEncoder)
    logger.debug(jstr)
    assert jstr == r'[{"$id": "1", "$values": {"Swimming": 1, "Video Games": 2, "Fishing": 3}}, {"$ref": "1"}]'