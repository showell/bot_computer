'''
This file configures the built-in bots, but it doesn't
implement their full behavior.
'''

def multiply(args):
    product = 1
    for arg in args:
        product = int(arg) * product
    return product

def make_builtin_bots(bot_builder):
    return {
        'ADD': bot_builder(
            name='ADD',
            compute_via_python = lambda args:
                sum(int(x) for x in args)
        ),
        'MULT': bot_builder(
            name='MULT',
            compute_via_python = lambda args:
                multiply(args)
        ),
    }

