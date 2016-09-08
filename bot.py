import json
from builtin import make_builtin_bots
from commands import COMMANDS
from calculate import Calculation
from translate import translate

class BuiltinBot:
    def __init__(self, name, compute_via_python):
        self.name = name
        self.compute_via_python = compute_via_python

    def receive(self, send_calculation, callback, program):
        calculation = Calculation(program, send_calculation)
        def on_callback(computed_args):
            callback(self.compute_via_python(*computed_args))
        calculation.compute_args(on_callback)

class IfBot:
    def receive(self, send_calculation, callback, program):
        assert program[0] == 'if'

        def send_calc(cb, program):
            # This can be send_calculation when we introduce RAW
            Calculation(program, send_calculation).compute(cb)

        args = program[1:]
        def my_callback(answer):
            if answer:
                send_calc(callback, args[1])
            else:
                send_calc(callback, args[2])
        send_calc(my_callback, args[0])

class ApplyBot:
    def receive(self, send_calculation, callback, program):
        action_program = program[1][0]
        args = program[1][1:]
        def my_callback(action):
            new_program = [action] + args
            send_calculation(callback, new_program)
        Calculation(action_program, send_calculation).compute(my_callback)

class DataBot:
    def receive(self, send_calculation, callback, program):
        callback(program[1])

class TranslateBot:
    def __init__(self, template_source, template_target):
        self.template_source = template_source
        self.template_target = template_target

    def receive(self, send_calculation, callback, program):
        calculation = Calculation(program, send_calculation)
        calculation.compute_args(
            lambda computed_args:
                self.compute(send_calculation, callback, computed_args))

    def compute(self, send_calculation, callback, computed_args):
        new_program = translate(
            template_source=self.template_source,
            template_target=self.template_target,
            args=computed_args)
        send_calculation(callback, new_program)

BOTS = make_builtin_bots(BuiltinBot)

for source, target in COMMANDS:
    name = source.split()[0]
    BOTS[name] = TranslateBot(template_source=source, template_target=target)

BOTS['if'] = IfBot()
BOTS['apply'] = ApplyBot()
BOTS['data'] = DataBot()

