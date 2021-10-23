

def assert_same_structure(nest1, nest2, check_types=True):
    'Asserts that two structures are nested in the same way.\n\n  Note that namedtuples with identical name and fields are always considered\n  to have the same shallow structure (even with `check_types=True`).\n  For intance, this code will print `True`:\n\n  ```python\n  def nt(a, b):\n    return collections.namedtuple(\'foo\', \'a b\')(a, b)\n  print(assert_same_structure(nt(0, 1), nt(2, 3)))\n  ```\n\n  Args:\n    nest1: an arbitrarily nested structure.\n    nest2: an arbitrarily nested structure.\n    check_types: if `True` (default) types of sequences are checked as well,\n        including the keys of dictionaries. If set to `False`, for example a\n        list and a tuple of objects will look the same if they have the same\n        size. Note that namedtuples with identical name and fields are always\n        considered to have the same shallow structure. Two types will also be\n        considered the same if they are both list subtypes (which allows "list"\n        and "_ListWrapper" from checkpointable dependency tracking to compare\n        equal).\n\n  Raises:\n    ValueError: If the two structures do not have the same number of elements or\n      if the two structures are not nested in the same way.\n    TypeError: If the two structures differ in the type of sequence in any of\n      their substructures. Only possible if `check_types` is `True`.\n  '
    try:
        _pywrap_tensorflow.AssertSameStructure(nest1, nest2, check_types)
    except (ValueError, TypeError) as e:
        str1 = str(map_structure((lambda _: _DOT), nest1))
        str2 = str(map_structure((lambda _: _DOT), nest2))
        raise type(e)(('%s\nEntire first structure:\n%s\nEntire second structure:\n%s' % (str(e), str1, str2)))
