import string
import re

class SgfTree(object):

    def __init__(self, properties=None, children=None):
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        if not isinstance(other, SgfTree):
            return False
        for k, v in self.properties.items():
            if k not in other.properties:
                return False
            if other.properties[k] != v:
                return False
        for k in other.properties.keys():
            if k not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for a, b in zip(self.children, other.children):
            if a != b:
                return False
        return True

    def __ne__(self, other):
        return not self == other


def parse(input_string):
    data_entry = input_string.replace('\\', '').replace('\t', ' ')
    regex = r'\(?\;?(?P<keys>[A-Z]+)?(?:\[(?P<values>(.|\s)+?\]?)\])'
    matches = re.finditer(regex, data_entry, re.MULTILINE)

    if input_string == '(;)':
        return SgfTree()

    if re.match(regex, input_string) is None:
        raise ValueError('You entered an invalid input, try again with a different one.')

    level, childs, last_key, properties = 0, [], '', {}
    for _, match in enumerate(matches, start=1):
        full = match.group()
        key = match.group('keys')
        value = match.group('values')

        if '(;' in full or ';' in full:
            if not key and not last_key or key not in string.ascii_uppercase or not value:
                raise ValueError('You entered an invalid input, try again with a different one.')
            level += 1

        if level == 1:
            if not key and last_key:
                properties[last_key].append(value)
            else:
                if key in properties:
                    properties[key].append(value)
                else:
                    properties[key] = [value]

        if level >= 2:
            childs.append(SgfTree({key: [value]}))

        if key:
            last_key = key

    return SgfTree(properties, childs)