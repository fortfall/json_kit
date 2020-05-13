import pytest
import json
import logging
from .conftest import Job
from ..SimpleJSONEncoder import SimpleJSONEncoder
from ..RefJSONEncoder import RefJSONEncoder
from ..AllRefJSONEncoder import AllRefJSONEncoder

logger = logging.getLogger(__name__)

class SlotPerson:
    __slots__ = ['name', 'age', 'job', 'hobbies']
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies

@pytest.fixture(params=[{'name': 'Jack', 'age': 33, 'job': Job.Teacher}])
def slot_person(request, hobbies):
    person = SlotPerson(**request.param, hobbies=hobbies)
    return person

def test_simple_encoder(slot_person):
    jstr1 = json.dumps(slot_person, cls=SimpleJSONEncoder)
    jstr2 = json.dumps(slot_person, cls=RefJSONEncoder)
    jstr3 = json.dumps(slot_person, cls=AllRefJSONEncoder)
    assert jstr1 == jstr2
    assert jstr1 == jstr3
    assert jstr2 == jstr3
    logger.debug(jstr1)
    assert jstr1 == r'{"name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}'



