import json
from enum import Enum
from .utils import (is_elemental, is_collection, is_custom_class)

class EasyJSONEncoder(json.JSONEncoder):
    remove_none_fields=True
    def default(self, obj):
        if isinstance(obj, (set)):
            return list(obj)
        if isinstance(obj, Enum):
            return obj.value
        if is_custom_class(obj):
            if EasyJSONEncoder.remove_none_fields:
                return {k: v for k, v in obj.__dict__.items() if v is not None}
            else:
                return obj.__dict__
        return obj