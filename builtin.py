'''
This file configures the simpler built-in bots, but it doesn't
implement their full behavior.

Simple built-in bots don't have introspection capability, and
they only now how to manipulate JSON; they don't call other bots.
'''

def do_add(args):
    assert len(args) >= 1
    sum = args[0]
    for arg in args[1:]:
        sum += arg
    return sum

def do_deref(args):
    return args[1][args[0]]

def do_eq(args):
    if str(args[0]) == str(args[1]):
        return 1
    else:
        return 0

def do_len(args):
    return len(args[0])

def do_list(args):
    return args

def do_multiply(args):
    assert len(args) >= 1
    product = args[0]
    for arg in args[1:]:
        product *= arg
    return product

def do_str(args):
    return str(args[0])

def make_builtin_bots(bot_builder):
    return {
        'ADD': bot_builder(
            name='ADD',
            compute_via_python = do_add
        ),
        'DEREF': bot_builder(
            name='DEREF',
            compute_via_python=do_deref
        ),
        'EQ': bot_builder(
            name='EQ',
            compute_via_python=do_eq
        ),
        'LEN': bot_builder(
            name='LEN',
            compute_via_python=do_len,
        ),
        'LIST': bot_builder(
            name='LIST',
            compute_via_python=do_list,
        ),
        'MULT': bot_builder(
            name='MULT',
            compute_via_python=do_multiply
        ),
        'STR': bot_builder(
            name='STR',
            compute_via_python=do_str
        ),
    }

