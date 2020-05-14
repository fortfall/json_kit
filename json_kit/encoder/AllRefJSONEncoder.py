import json
from collections import OrderedDict
from enum import Enum
from json.encoder import (_make_iterencode, JSONEncoder,
                          encode_basestring_ascii, INFINITY,
                          c_make_encoder, encode_basestring)
from .utils import (is_elemental, is_collection,
                    is_customized_class, hashable, to_hashable)
from .RefJSONEncoder import RefJSONEncoder

class AllRefJSONEncoder(RefJSONEncoder):
    def _count_ref(self, obj):
        if is_elemental(obj):
            return
        if is_collection(obj):
            if isinstance(obj, (list, tuple, set, frozenset)):
                k = to_hashable(obj)
                if k in self.vec_ref_cnt:
                    self.vec_ref_cnt[k] += 1
                else:
                    self.vec_ref_cnt[k] = 1
            elif isinstance(obj, dict):
                k = to_hashable(obj)
                if k in self.dict_ref_cnt:
                    self.dict_ref_cnt[k] += 1
                else:
                    self.dict_ref_cnt[k] = 1
            self._count_ref_in_collection(obj)
        elif is_customized_class(obj) and hashable(obj):
            if obj in self.cls_ref_cnt:
                self.cls_ref_cnt[obj] += 1
            else:
                self.cls_ref_cnt[obj] = 1
            self._count_ref_in_cls(obj)
    
    def _prepare(self, obj):
        self.vec_ref_cnt = {}
        self.vec_ref_serialized = {}
        self.dict_ref_cnt = {}
        self.dict_ref_serialized = {}
        super()._prepare(obj)

    def default(self, obj):
        if isinstance(obj, set):
            converted = list(obj)
            converted.sort(key=lambda x: id(x))
            return converted
        elif isinstance(obj, Enum):
            return obj.value
        # elif is_customized_class(obj):
        return obj

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        self._prepare(o)
        self._count_ref(o)
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring

        def floatstr(o, allow_nan=self.allow_nan,
                _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text


        # Disable c_make_encoder
        if (False and _one_shot and c_make_encoder is not None
                and self.indent is None):
            _iterencode = c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan)
        else:
            _iterencode = self._make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot)
        return _iterencode(o, 0)

    def _make_iterencode(self, markers, _default, _encoder, _indent, _floatstr,
            _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot,
            ## HACK: hand-optimized bytecode; turn globals into locals
            ValueError=ValueError,
            dict=dict,
            float=float,
            id=id,
            int=int,
            isinstance=isinstance,
            list=list,
            str=str,
            tuple=tuple,
            _intstr=int.__str__,
        ):

        if _indent is not None and not isinstance(_indent, str):
            _indent = ' ' * _indent
        
        def _iterencode_list_ref(lst, _current_indent_level):
            k = to_hashable(lst)
            if k not in self.vec_ref_cnt or self.vec_ref_cnt[k] <= 1:
                yield from _iterencode_list(lst, _current_indent_level)
            elif k in self.vec_ref_serialized:
                converted = { "$ref": str(self.vec_ref_serialized[k]) }
                yield from _iterencode_dict(converted, _current_indent_level)
            elif self.vec_ref_cnt[k] > 1:
                self.ref_id += 1
                self.vec_ref_serialized[k] = self.ref_id

                converted = OrderedDict()
                converted["$id"] = str(self.ref_id)
                converted["$values"] = lst
                yield from _iterencode_dict(converted, _current_indent_level, reduce_level=True)
            else:
                raise Exception("Unhandled obj in _iterencode_list_ref")
        
        def _iterencode_dict_ref(dct, _current_indent_level):
            k = to_hashable(dct)
            if k not in self.dict_ref_cnt or self.dict_ref_cnt[k] <= 1:
                yield from _iterencode_dict(dct, _current_indent_level)
            elif k in self.dict_ref_serialized:
                converted = { "$ref": str(self.dict_ref_serialized[k]) }
                yield from _iterencode_dict(converted, _current_indent_level)
            elif self.dict_ref_cnt[k] > 1:
                self.ref_id += 1
                self.dict_ref_serialized[k] = self.ref_id
                converted = OrderedDict()
                converted["$id"] = str(self.ref_id)
                converted["$values"] = dct
                yield from _iterencode_dict(converted, _current_indent_level, reduce_level=True)
            else:
                raise Exception("Unhandled obj in _iterencode_dict_ref")
        
        def _iterencode_cls_ref(cls, _current_indent_level):
            if not hashable(cls) or cls not in self.cls_ref_cnt or self.cls_ref_cnt[cls] <= 1:
                converted = self._cls_to_dict(cls, skip_none_fields=AllRefJSONEncoder.skip_none_fields,
                                serialize_only_annotated=AllRefJSONEncoder.serialize_only_annotated)
                yield from _iterencode_dict(converted, _current_indent_level)
            elif cls in self.cls_ref_serialized:
                converted = { "$ref": str(self.cls_ref_serialized[cls]) }
                yield from _iterencode_dict(converted, _current_indent_level)
            elif self.cls_ref_cnt[cls] > 1:
                self.ref_id += 1
                self.cls_ref_serialized[cls] = self.ref_id
                converted = OrderedDict()
                converted["$id"] = str(self.ref_id)
                converted = self._cls_to_dict(cls, skip_none_fields=AllRefJSONEncoder.skip_none_fields, 
                                serialize_only_annotated=AllRefJSONEncoder.serialize_only_annotated, dct=converted)
                yield from _iterencode_dict(converted, _current_indent_level)
            else:
                raise Exception("Unhandled custom class obj in _iterencode_cls_ref")

        def _iterencode_list(lst, _current_indent_level, reduce_level=False):
            if not lst:
                yield '[]'
                return
            if markers is not None:
                markerid = id(lst)
                if markerid in markers:
                    raise ValueError("Circular reference detected")
                markers[markerid] = lst
            buf = '['
            if _indent is not None:
                _current_indent_level += 1
                newline_indent = '\n' + _indent * _current_indent_level
                separator = _item_separator + newline_indent
                buf += newline_indent
            else:
                newline_indent = None
                separator = _item_separator
            first = True
            for value in lst:
                if first:
                    first = False
                else:
                    buf = separator
                if isinstance(value, str):
                    yield buf + _encoder(value)
                elif value is None:
                    yield buf + 'null'
                elif value is True:
                    yield buf + 'true'
                elif value is False:
                    yield buf + 'false'
                elif isinstance(value, int):
                    # Subclasses of int/float may override __str__, but we still
                    # want to encode them as integers/floats in JSON. One example
                    # within the standard library is IntEnum.
                    yield buf + _intstr(value)
                elif isinstance(value, float):
                    # see comment above for int
                    yield buf + _floatstr(value)
                else:
                    yield buf
                    if reduce_level and isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    elif reduce_level and isinstance(value, dict):
                        chunks = _iterencode_dict(value, _current_indent_level)
                    else:
                        chunks = _iterencode(value, _current_indent_level)
                    yield from chunks
            if newline_indent is not None:
                _current_indent_level -= 1
                yield '\n' + _indent * _current_indent_level
            yield ']'
            if markers is not None:
                del markers[markerid]

        def _iterencode_dict(dct, _current_indent_level, reduce_level=False):
            if not dct:
                yield '{}'
                return
            if markers is not None:
                markerid = id(dct)
                if markerid in markers:
                    raise ValueError("Circular reference detected")
                markers[markerid] = dct
            yield '{'
            if _indent is not None:
                _current_indent_level += 1
                newline_indent = '\n' + _indent * _current_indent_level
                item_separator = _item_separator + newline_indent
                yield newline_indent
            else:
                newline_indent = None
                item_separator = _item_separator
            first = True
            if _sort_keys:
                items = sorted(dct.items(), key=lambda kv: kv[0])
            else:
                items = dct.items()
            for key, value in items:
                if isinstance(key, str):
                    pass
                # JavaScript is weakly typed for these, so it makes sense to
                # also allow them.  Many encoders seem to do something like this.
                elif isinstance(key, float):
                    # see comment for int/float in _make_iterencode
                    key = _floatstr(key)
                elif key is True:
                    key = 'true'
                elif key is False:
                    key = 'false'
                elif key is None:
                    key = 'null'
                elif isinstance(key, int):
                    # see comment for int/float in _make_iterencode
                    key = _intstr(key)
                elif _skipkeys:
                    continue
                else:
                    raise TypeError(f'keys must be str, int, float, bool or None, '
                                    f'not {key.__class__.__name__}')
                if first:
                    first = False
                else:
                    yield item_separator
                yield _encoder(key)
                yield _key_separator
                if isinstance(value, str):
                    yield _encoder(value)
                elif value is None:
                    yield 'null'
                elif value is True:
                    yield 'true'
                elif value is False:
                    yield 'false'
                elif isinstance(value, int):
                    # see comment for int/float in _make_iterencode
                    yield _intstr(value)
                elif isinstance(value, float):
                    # see comment for int/float in _make_iterencode
                    yield _floatstr(value)
                else:
                    if reduce_level and isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    elif reduce_level and isinstance(value, dict):
                        chunks = _iterencode_dict(value, _current_indent_level)
                    else:
                        chunks = _iterencode(value, _current_indent_level)
                    yield from chunks
            if newline_indent is not None:
                _current_indent_level -= 1
                yield '\n' + _indent * _current_indent_level
            yield '}'
            if markers is not None:
                del markers[markerid]

        def _iterencode(o, _current_indent_level):
            if isinstance(o, str):
                yield _encoder(o)
            elif o is None:
                yield 'null'
            elif o is True:
                yield 'true'
            elif o is False:
                yield 'false'
            elif isinstance(o, int):
                # see comment for int/float in _make_iterencode
                yield _intstr(o)
            elif isinstance(o, float):
                # see comment for int/float in _make_iterencode
                yield _floatstr(o)
            elif isinstance(o, (list, tuple)):
                yield from _iterencode_list_ref(o, _current_indent_level)
            elif isinstance(o, dict):
                yield from _iterencode_dict_ref(o, _current_indent_level)
            else:
                if markers is not None:
                    markerid = id(o)
                    if markerid in markers:
                        raise ValueError("Circular reference detected")
                    markers[markerid] = o
                if is_customized_class(o):
                    yield from _iterencode_cls_ref(o, _current_indent_level)
                else:
                    o = _default(o)
                    yield from _iterencode(o, _current_indent_level)
                if markers is not None:
                    del markers[markerid]
        return _iterencode