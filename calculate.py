'''
The classes here don't know to compute anything; instead,
they know how to orchestrate a calculation.  In particular,
they know how to get values for arguments, which sometimes
requires dispatching another actor to do work.

The Calculation class doesn't know internally how to send
a calculation to another actor; it gets passed in a
send_calculation message.
'''

def make_arg(token, send_calculation):
    if token.kind == 'literal':
        return Literal(token)
    else:
        return Calculation(token, send_calculation)

class Literal:
    def __init__(self, token):
        self.val = int(token.val)

    def compute(self, callback):
        callback(self.val)

class Calculation:
    def __init__(self, token, send_calculation):
        self.token = token
        tokens = token.tokens[:]
        action = tokens.pop(0)
        assert action.kind == 'literal'
        self.action = str(action)
        self.args = [make_arg(t, send_calculation) for t in tokens]
        self.send_calculation = send_calculation

    def compute(self, callback):
        self.send_calculation(callback, self.token)

    def compute_args(self, callback):
        computed_args = []

        def on_computed_arg(computed_arg):
            computed_args.append(computed_arg)
            compute_one()

        def compute_one():
            if len(computed_args) == len(self.args):
                callback(computed_args)
            else:
                arg = self.args[len(computed_args)]
                arg.compute(on_computed_arg)

        compute_one()

