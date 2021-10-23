def convert_and_compare(x, Type):
    '\n    Convert x to be the same type as Type and then convert back to\n    check whether there is a loss of information\n    :param x: object to be checked\n    :param Type: target type to check x over\n\n    '
    return (type(x)(Type(x)) == x)