'''
This file implements primitive functions that only act
on data and don't interact with other functions.
'''

BUILTINS = []

def public(f):
    BUILTINS.append(f)
    return f

@public
def do_add(*args):
    assert len(args) >= 1
    sum = args[0]
    for arg in args[1:]:
        sum += arg
    return sum

@public
def do_deref(index, data):
    return data[index]

@public
def do_eq(a, b):
    if a == b:
        return 1
    else:
        return 0

@public
def do_len(val):
    return len(val)

@public
def do_list(*items):
    return list(items)

@public
def do_multiply(*args):
    assert len(args) >= 1
    product = args[0]
    for arg in args[1:]:
        product *= arg
    return product

@public
def do_range(lo, hi):
    return range(lo, hi)

@public
def do_str(val):
    return str(val)

