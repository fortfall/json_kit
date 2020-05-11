from enum import Enum


def is_elemental(obj):
    return isinstance(obj, (int, float, Enum))

def is_collection(obj):
    return isinstance(obj, (list, dict, tuple, set))

def is_custom_class(obj):
    return not isinstance(obj, (int, float, Enum, list, dict, tuple, set)) and hasattr(obj, "__dict__")

def hashable(obj):
    try:
        hash(obj)
    except TypeError:
        return False
    return True

def to_hashable(obj):
    if isinstance(obj, (list, tuple)):
        return list_to_hashable(obj)
    elif isinstance(obj, dict):
        return dict_to_hashable(obj)
    elif isinstance(obj, set):
        return set_to_hashable(obj)
    else:
        return id(obj)

def set_to_hashable(obj):
    converted = list(obj)
    converted.sort(key=lambda x: id(x))
    return list_to_hashable(converted)

def list_to_hashable(obj):
    return tuple(item if hashable(item) else id(item) for item in obj)

def dict_to_hashable(obj):
    converted = [(k, v) for k, v in obj.items()]
    converted.sort(key=lambda x: id(x[0]))
    keys = tuple(x[0] if hashable(x[0]) else id(x[0]) for x in converted)
    values = tuple(x[1] if hashable(x[1]) else id(x[1]) for x in converted)
    return (keys, values)