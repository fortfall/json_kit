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