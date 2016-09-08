from bot import BOTS
from vm import VirtualMachine
import json

def run():
    messages = [
        '["ADD", [null, 1], [null, 2]]',
        '["ADD", [null, [1, 2]], [null, [3, 4]]]',
        '["DOUBLE", [null, 13]]',
        '["SQUARE", ["ADD", [null, 3], [null, 4]]]',
        '["DOUBLE", ["DOUBLE", [null, 5]]]',
        '["TAG", [null, "td"], [null, "hello world"]]',
        '["RANGE", [null, 5], ["ADD", [null, 5], [null, 10]]]',
        '["LIST", [null, 5], [null, 7], ["ADD", [null, 8], [null, 1]]]',
        '["LEN", [null, [0,1,2,3,4]]]',
        '["DEREF", [null, 2], [null, ["apple", "banana", "carrot", "dog"]]]',
        '["DEREF", [null, "x"], [null, {"x": 5, "y": 7}]]',
        '["IS_ZERO", [null, 5]]',
        '["IS_ZERO", ["ADD", [null, 3], [null, -3]]]',
        '["INCR", [null, 10]]',
        '["DECR", [null, 10]]',
        '["IF", [null, 1], [null, "if-case"], [null, "else-case"]]',
        '''
        [
            "IF",
            ["EQ", [null, "x"], [null, "y"]],
            [null, "if-case"],
            [null, "else-case"]
        ]
        ''',
        '["FACTORIAL", [null, 5]]',
        '["MATH_ROW", [null, 7]]',
        '["TD", [null, "hello"]]',
        '["CONCAT", [null, ["a", "b", "c"]]]',
        '["TR", ["LIST", ["TD", [null, "a"]], [null, "<td>b</td>"]]]',
        '["APPLY", [[null, "ADD"], [null, 1], [null, 2]]]',
        '["MAP", [null, [1, 2, 3]], [null, "DOUBLE"]]',
        '["MATH_TR", [null, 7]]',
        '["MATH_TABLE_GUTS", ["RANGE", [null, 5], [null, 12]]]',
        '["TABLE", [null, "header_row"], [null, ["foo", "bar"]]]',
    ]

    for message in messages:
        vm = VirtualMachine(BOTS)

        def callback(answer):
            print '%s ->\n    %s\n' % (message, str(answer))

        vm.process_message(callback, message)

    def write_html(answer):
        open('foo.html', 'w').write(answer)

    vm.process_message(write_html,
        '["MATH_TABLE", ["RANGE", [null, 5], [null, 14]]]')

if __name__ == '__main__':
    run()
