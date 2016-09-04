'''
This file configures the built-in bots, but it doesn't
implement their full behavior.
'''

def do_add(args):
    sum = 0
    for arg in args:
        sum = int(arg) + sum
    return sum

def do_multiply(args):
    product = 1
    for arg in args:
        product = int(arg) * product
    return product

CNT = 1
def do_eq(args):
    global CNT
    CNT += 1
    print args
    print 'args', args
    if CNT == 8:
        print 'exiting'
        import sys; sys.exit()
    if str(args[0]) == str(args[1]):
        return 1
    else:
        return 0

def make_builtin_bots(bot_builder):
    return {
        'ADD': bot_builder(
            name='ADD',
            compute_via_python = do_add
        ),
        'MULT': bot_builder(
            name='MULT',
            compute_via_python=do_multiply
        ),
        'EQ': bot_builder(
            name='EQ',
            compute_via_python=do_eq
        ),
    }

