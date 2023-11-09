from functools import reduce
from mangust228.exceptions import EmptyFileName


def foo(hello: str, *file_name):
    if not file_name:
        raise EmptyFileName("jopa")
    result = reduce(lambda a, b: f"{a}_{b}", file_name)
    print(type(result))


foo("world", 1)
