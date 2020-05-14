import json
import logging
import pytest
from typing import List
from .conftest import Job
from ..SimpleJSONEncoder import SimpleJSONEncoder
from ..RefJSONEncoder import RefJSONEncoder
from ..AllRefJSONEncoder import AllRefJSONEncoder

logger = logging.getLogger(__name__)

class AnnotatedPerson:
    name: str
    age: int
    job: Job
    hobbies: List[str]
    def __init__(self, name, age, job, hobbies, address):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
        self.address = address

@pytest.fixture(params=[{'name': 'Jack', 'age': 33, 'job': Job.Teacher, 'address': 'ChengDu'}])
def annotated_person(request, hobbies):
    person = AnnotatedPerson(**request.param, hobbies=hobbies)
    return person

def test_annotated_person(annotated_person):
    SimpleJSONEncoder.serialize_only_annotated = True
    jstr1 = json.dumps(annotated_person, cls=SimpleJSONEncoder)
    RefJSONEncoder.serialize_only_annotated = True
    jstr2 = json.dumps(annotated_person, cls=RefJSONEncoder)
    AllRefJSONEncoder.serialize_only_annotated = True
    jstr3 = json.dumps(annotated_person, cls=AllRefJSONEncoder)
    logger.debug(jstr1)
    assert jstr1 == jstr2
    assert jstr1 == jstr3
    assert jstr2 == jstr3
    assert jstr1 == r'{"name": "Jack", "age": 33, "job": 0, "hobbies": ["Swimming", "Video Games", "Fishing"]}'
