import json
from collections import OrderedDict
from enum import Enum
from .SimpleJSONEncoder import SimpleJSONEncoder
from .utils import (is_elemental, is_collection, 
                    is_customized_class, hashable)

class RefJSONEncoder(SimpleJSONEncoder):
    def _count_ref(self, obj):
        if is_elemental(obj):
            return
        elif is_collection(obj):
            self._count_ref_in_collection(obj)
        elif is_customized_class(obj) and hashable(obj):
            if obj in self.cls_ref_cnt:
                self.cls_ref_cnt[obj] += 1
            else:
                self.cls_ref_cnt[obj] = 1
            self._count_ref_in_cls(obj)

    def _count_ref_in_collection(self, obj):
        if len(obj) == 0:
            return
        if isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                self._count_ref(item)
        elif isinstance(obj, (dict)):
            for k, v in obj.items():
                self._count_ref(v)
    
    def _count_ref_in_cls(self, obj):
        if hasattr(obj, '__dict__'):
            for name, value in obj.__dict__.items():
                self._count_ref(value)
        elif hasattr(obj, '__slots__'):
            for x in obj.__slots__:
                self._count_ref(getattr(obj, x))

    def _prepare(self, o):
        self.cls_ref_cnt = {}  # ref: count
        self.cls_ref_serialized = {}  # ref: id
        self.ref_id = 0
    
    def encode(self, o):
        return super().encode(o)

    def iterencode(self, o, _one_shot=False):
        self._prepare(o)
        self._count_ref(o)
        return super().iterencode(o, _one_shot)
    
    def default(self, obj):
        if isinstance(obj, (set)):
            return list(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif is_customized_class(obj):
            return self._process_customized_cls(obj)
        return obj
    
    def _process_customized_cls(self, obj):
        if not hashable(obj) or obj not in self.cls_ref_cnt or self.cls_ref_cnt[obj] <= 1:
            return self._cls_to_dict(obj, skip_none_fields=RefJSONEncoder.skip_none_fields,
                    serialize_only_annotated=RefJSONEncoder.skip_none_fields)
        elif obj in self.cls_ref_serialized:
            return {
                "$ref": str(self.cls_ref_serialized[obj])
            }
        elif self.cls_ref_cnt[obj] > 1:
            self.ref_id += 1
            self.cls_ref_serialized[obj] = self.ref_id
            out = OrderedDict()
            out["$id"] = str(self.ref_id)
            return self._cls_to_dict(obj, skip_none_fields=RefJSONEncoder.skip_none_fields, 
                        serialize_only_annotated=RefJSONEncoder.serialize_only_annotated, dct=out)
            return out
        else:
            raise Exception("Unhandled custom class obj in _process_customized_cls")