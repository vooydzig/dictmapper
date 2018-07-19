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
            target[dest_path_expr.fields[0]] = value
        else:
            path, node = dest_path_expr.left, dest_path_expr.right
            while hasattr(path, 'left'):
                value = {node.fields[0]: value}
                path, node = path.left, path.right
            target[path.fields[0]] = {node.fields[0]: value}

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
