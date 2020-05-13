import pytest
from json_kit.encoder.utils import (is_elemental, is_collection,
                                    is_customized_class)
from .conftest import Job, Person


@pytest.fixture(params=[True, False])
def bool_var(request):
    return request.param

@pytest.fixture(params=[1.2, 0.01, 4.5])
def float_var(request):
    return request.param

@pytest.fixture(params=[0, 2, 100])
def int_var(request):
    return request.param

@pytest.fixture(params=[Job.Teacher, Job.Engineer])
def enum_var(request):
    return request.param

@pytest.fixture(params=[[], [1, 'a'], ['', None]])
def list_var(request):
    return request.param

@pytest.fixture(params=[(), (1, 'a'), ('', None)])
def tuple_var(request):
    return request.param

@pytest.fixture(params=[{}, {'a': 1, 'b': 2}, {3: 5}])
def dict_var(request):
    return request.param

@pytest.fixture(params=[{'a'}, {1, 2, 3}])
def set_var(request):
    return request.param

def test_bool(bool_var):
    assert is_elemental(bool_var)
    assert not is_collection(bool_var)
    assert not is_customized_class(bool_var)

def test_int(int_var):
    assert is_elemental(int_var)
    assert not is_collection(int_var)
    assert not is_customized_class(int_var)

def test_float(float_var):
    assert is_elemental(float_var)
    assert not is_collection(float_var)
    assert not is_customized_class(float_var)

def test_enum(enum_var):
    assert is_elemental(enum_var)
    assert not is_collection(enum_var)
    assert not is_customized_class(enum_var)

def test_list(list_var):
    assert not is_elemental(list_var)
    assert is_collection(list_var)
    assert not is_customized_class(list_var)

def test_tuple(tuple_var):
    assert not is_elemental(tuple_var)
    assert is_collection(tuple_var)
    assert not is_customized_class(tuple_var)

def test_dict(dict_var):
    assert not is_elemental(dict_var)
    assert is_collection(dict_var)
    assert not is_customized_class(dict_var)

def test_set(set_var):
    assert not is_elemental(set_var)
    assert is_collection(set_var)
    assert not is_customized_class(set_var)

def test_customized_class(person):
    assert not is_elemental(person)
    assert not is_collection(person)
    assert is_customized_class(person)



