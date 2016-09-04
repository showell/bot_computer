'''
This file configures the built-in bots, but it doesn't
implement their full behavior.
'''

def multiply(args):
    product = 1
    for arg in args:
        product = int(arg) * product
    return product

def do_if(args):
    cond = True
    if args[0] in ['0', 'false', '""']:
        cond = False
    if cond:
        return args[1]
    else:
        return args[2]

def make_builtin_bots(bot_builder):
    return {
        'ADD': bot_builder(
            name='ADD',
            compute_via_python = lambda args:
                sum(int(x) for x in args)
        ),
        'MULT': bot_builder(
            name='MULT',
            compute_via_python = multiply
        ),
        'IF': bot_builder(
            name='IF',
            compute_via_python = do_if
        ),
    }

