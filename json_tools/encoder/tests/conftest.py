from enum import Enum
import pytest
from json_tools.encoder import (is_custom_class, hashable, to_hashable)


class Job(Enum):
    Teacher = 0
    Engineer = 1
    Doctor = 2
    Actor = 3

class Person:
    def __init__(self, name, age, job, hobbies):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
    
    def __hash__(self):
        data = [(k, v) if hashable(v) else (k, to_hashable(v)) for k, v in self.__dict__.items()]
        data.sort(key=lambda x: x[0])
        data = tuple(data)
        return hash(data)
    
    def __eq__(self, other):
        if not is_custom_class(other) or not hashable(other):
            return False
        return self.__class__ == other.__class__ and self.__hash__() == other.__hash__()

@pytest.fixture(params=[0, 1, 2])
def enums(request):
    return Job(request.param)


@pytest.fixture(params=[[0], [1, 2], [1, 2, 3]])
def enum_list(request):
    return [Job(x) for x in request.param]

@pytest.fixture()
def hobbies(request):
    return ['Swimming', 'Video Games', 'Fishing']

@pytest.fixture()
def another_hobbies(request):
    return ['Swimming', 'Video Games', 'Fishing']

@pytest.fixture()
def hobby_list(hobbies, another_hobbies):
    return [hobbies, another_hobbies]

@pytest.fixture()
def hobby_time(request):
    htime = {
        'Swimming': 1,
        'Video Games': 2,
        'Fishing': 3
    }
    return htime

@pytest.fixture()
def another_hobby_time(request):
    htime = {
        'Swimming': 1,
        'Fishing': 3,
        'Video Games': 2
    }
    return htime

@pytest.fixture()
def hobby_time_list(hobby_time, another_hobby_time):
    return [hobby_time, another_hobby_time]

@pytest.fixture(params=[['Jack', 33, Job.Teacher]])
def person(request, hobbies):
    return Person(request.param[0], request.param[1], request.param[2], hobbies)

@pytest.fixture(params=[['Jack', 33, Job.Teacher]])
def another_person(request, another_hobbies):
    return Person(request.param[0], request.param[1], request.param[2], another_hobbies)

@pytest.fixture(params=[['Mike', 24, Job.Doctor]])
def person_with_same_hobbies(request, hobbies):
    return Person(request.param[0], request.param[1], request.param[2], hobbies)

@pytest.fixture()
def person_list(person, another_person):
    return [person, another_person]

@pytest.fixture()
def persons_with_same_hobbies(person, another_person, person_with_same_hobbies):
    return [person, another_person, person_with_same_hobbies]

@pytest.fixture
def person_with_none_fields(person):
    person.age = None
    return person
