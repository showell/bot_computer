'''
This file configures the simpler built-in bots, but it doesn't
implement their full behavior.

Simple built-in bots don't have introspection capability, and
they only now how to manipulate JSON; they don't call other bots.
'''

def do_add(*args):
    assert len(args) >= 1
    sum = args[0]
    for arg in args[1:]:
        sum += arg
    return sum

def do_deref(index, data):
    return data[index]

def do_eq(a, b):
    if a == b:
        return 1
    else:
        return 0

def do_len(val):
    return len(val)

def do_list(*items):
    return list(items)

def do_multiply(*args):
    assert len(args) >= 1
    product = args[0]
    for arg in args[1:]:
        product *= arg
    return product

def do_range(lo, hi):
    return range(lo, hi)

def do_str(val):
    return str(val)

def make_builtin_bots(bot_builder):
    tups = [
        ('ADD', do_add),
        ('DEREF', do_deref),
        ('EQ', do_eq),
        ('LEN', do_len),
        ('LIST', do_list),
        ('MULT', do_multiply),
        ('RANGE', do_range),
        ('STR', do_str),
    ]

    return {name: bot_builder(name=name, compute_via_python=do_it) for
        name, do_it in tups}
