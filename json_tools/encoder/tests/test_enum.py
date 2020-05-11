import json
import pytest
import logging
from json_tools.encoder import SimpleJSONEncoder

logger = logging.getLogger(__name__)

def test_enums(enums):
    jstr = json.dumps(enums, cls=SimpleJSONEncoder)
    assert jstr == str(enums.value)

def test_enum_list(enum_list):
    jstr = json.dumps(enum_list, cls=SimpleJSONEncoder)
    logger.debug(jstr)
    int_list = [x.value for x in enum_list]
    assert jstr == str(int_list)