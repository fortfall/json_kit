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
            return self._cls_to_dict(obj, SimpleJSONEncoder.skip_none_fields)
        return obj
    
    def _cls_to_dict(self, obj, skip_none_fields=True, dct=None):
        if dct is None:
            dct = {}
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                if skip_none_fields and v is None:
                    continue
                dct[k] = v
        elif hasattr(obj, '__slots__'):
            for x in obj.__slots__:
                value = getattr(obj, x)
                if SimpleJSONEncoder.skip_none_fields and value is None:
                    continue
                dct[x] = value
        return dct