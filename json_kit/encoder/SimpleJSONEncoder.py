import json
import logging
from enum import Enum
from .utils import (is_elemental, is_collection, is_customized_class)

logger = logging.getLogger(__name__)

class SimpleJSONEncoder(json.JSONEncoder):
    skip_none_fields=True
    serialize_only_annotated=False
    def default(self, obj):
        if isinstance(obj, (set)):
            return list(obj)
        if isinstance(obj, Enum):
            return obj.value
        if is_customized_class(obj):
            return self._cls_to_dict(obj, skip_none_fields=SimpleJSONEncoder.skip_none_fields,
                            serialize_only_annotated=SimpleJSONEncoder.serialize_only_annotated)
        return obj
    
    def _cls_to_dict(self, obj, skip_none_fields=True, serialize_only_annotated=False, dct=None):
        if dct is None:
            dct = {}
        annotated = False
        if serialize_only_annotated and hasattr(obj.__class__, '__annotations__'):
            annotated = True
            annotations = obj.__class__.__annotations__
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                if skip_none_fields and v is None:
                    continue
                if annotated and k not in annotations:
                    continue
                dct[k] = v
        elif hasattr(obj, '__slots__'):
            for x in obj.__slots__:
                value = getattr(obj, x)
                if SimpleJSONEncoder.skip_none_fields and value is None:
                    continue
                if annotated and x in annotations:
                    continue
                dct[x] = value
        return dct