'''
The classes here don't know to compute anything; instead,
they know how to orchestrate a calculation.  In particular,
they know how to get values for arguments, which sometimes
requires dispatching another actor to do work.

The Calculation class doesn't know internally how to send
a calculation to another actor; it gets passed in a
send_calculation message.
'''

class Calculation:
    def __init__(self, program, send_calculation):
        self.program = program
        self.args = program[1:]
        self.send_calculation = send_calculation

    def compute(self, callback):
        if self.program[0] is None:
            # This should go away with RAW
            callback(self.args[0])
        else:
            self.send_calculation(callback, self.program)

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
                arg_calculation = Calculation(arg, self.send_calculation)
                arg_calculation.compute(on_computed_arg)

        compute_one()

