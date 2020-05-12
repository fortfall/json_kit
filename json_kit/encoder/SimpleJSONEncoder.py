import json
from enum import Enum
from .utils import (is_elemental, is_collection, is_customized_class)

class SimpleJSONEncoder(json.JSONEncoder):
    skip_none_fields=True
    def default(self, obj):
        if isinstance(obj, (set)):
            return list(obj)
        if isinstance(obj, Enum):
            return obj.value
        if is_customized_class(obj):
            if SimpleJSONEncoder.skip_none_fields:
                return {k: v for k, v in obj.__dict__.items() if v is not None}
            else:
                return obj.__dict__
        return obj