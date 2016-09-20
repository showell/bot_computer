import json
from builtin import BUILTINS
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

        args = program[1:]
        def my_callback(answer):
            if answer:
                send_calculation(callback, args[1])
            else:
                send_calculation(callback, args[2])
        send_calculation(my_callback, args[0])

class ApplyBot:
    def receive(self, send_calculation, callback, program):
        action_program = program[1][0]
        args = program[1][1:]
        def my_callback(action):
            new_program = [action] + args
            send_calculation(callback, new_program)
        send_calculation(my_callback, action_program)

class DataBot:
    def receive(self, send_calculation, callback, program):
        callback(program[1])

class MapBot:
    def receive(self, send_calculation, callback, program):
        action_program = program[2]
        list_program = program[1]

        def on_action(action):
            def on_list(my_list):
                result = []

                def on_mapped_item(mapped_item):
                    result.append(mapped_item)
                    compute_one()

                def compute_one():
                    if len(result) == len(my_list):
                        callback(result)
                    else:
                        item = my_list[len(result)]
                        program = [action, ['data', item]]
                        send_calculation(on_mapped_item, program)

                compute_one()

            send_calculation(on_list, list_program)

        send_calculation(on_action, action_program)


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

BOTS = {}
for f in BUILTINS:
    name = f.__name__
    if name.startswith('do_'):
        name = name[3:]
    BOTS[name] = BuiltinBot(name=name, compute_via_python=f)

for source, target in COMMANDS:
    name = source.split()[0]
    BOTS[name] = TranslateBot(template_source=source, template_target=target)

BOTS['apply'] = ApplyBot()
BOTS['data'] = DataBot()
BOTS['if'] = IfBot()
BOTS['map'] = MapBot()

