import jsonpath_rw

from collections import namedtuple

Mapping = namedtuple('Mapping', ['source', 'destination', 'transform'])


class JSONMapper:
    def __init__(self, mapping):
        self.mapping = mapping

    def map(self, source):
        target = self._get_empty_target_object(source)
        for src, dst, trans in self.mapping:
            if trans is None:
                trans = (lambda x: x)
            matches = jsonpath_rw.parse(src).find(source)
            if not matches or len(matches) > 1:
                continue
            value = trans(matches[0].value)
            if isinstance(target, dict):
                self.set_value(target, jsonpath_rw.parse(dst), value)
            else:
                target = value
                break
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
