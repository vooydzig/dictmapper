import jsonpath_rw

from collections import namedtuple

Mapping = namedtuple('Mapping', ['source', 'destination', 'transform'])


class JSONMapper:
    def __init__(self, mapping):
        self.mapping = self._normalize_mapping(mapping)

    def _normalize_mapping(self, mapping):
        normalized = []
        for src, dst, trans in mapping:
            if trans is None:
                trans = (lambda x: x)
            normalized.append(Mapping(src, dst, trans))
        return normalized

    def map(self, source):
        target = self._get_empty_target_object(source)
        for src, dst, trans in self.mapping:
            matches = jsonpath_rw.parse(src).find(source)
            if not matches:
                continue
            if len(matches) == 1:
                value = trans(matches[0].value)
            else:
                value = [trans(m.value) for m in matches]
            if isinstance(jsonpath_rw.parse(dst), jsonpath_rw.Root):
                target = self.set_root_value(target, value)
            else:
                self.set_value(target, jsonpath_rw.parse(dst), value)
        return target

    def set_value(self, target, dest_path_expr, value=None):
        if hasattr(dest_path_expr, 'fields'):
            self._set_value_to_field(target, dest_path_expr.fields[0], value)
        else:
            path, node = dest_path_expr.left, dest_path_expr.right
            if isinstance(node, jsonpath_rw.Slice):
                self.set_value(target, path, value=[value])
            else:
                self.set_value(target, path, value={node.fields[0]: value})

    def _set_value_to_field(self, target, path, value):
        if target.get(path) is None:
            target[path] = value
        else:
            self._merge_inputs(target, path, value)

    def set_root_value(self, target, value):
        try:
            target.update(value)
        except:
            target = value
        return target

    def _merge_inputs(self, target, target_field, value):
        if isinstance(target[target_field], type(value)):
            try:
                for item in target[target_field]:
                    item.update(value[0])
            except:
                try:
                    target[target_field].update(value)
                except:
                    target[target_field] = value
        else:
            target[target_field] = value

    def _get_empty_target_object(self, source):
        if not source:
            return source
        for src, dst, _, in self.mapping:
            if dst == '$':
                matches = jsonpath_rw.parse(src).find(source)
                if not matches or len(matches) > 1:
                    return {}
                return type(matches[0].value)()
            return {}
