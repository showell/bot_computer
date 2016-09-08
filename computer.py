from bot import BOTS
from vm import VirtualMachine

def run():
    programs = [
        ["ADD", [None, 1], [None, 2]],
        ["ADD", [None, [1, 2]], [None, [3, 4]]],
        ["DOUBLE", [None, 13]],
        ["SQUARE", ["ADD", [None, 3], [None, 4]]],
        ["DOUBLE", ["DOUBLE", [None, 5]]],
        ["TAG", [None, "td"], [None, "hello world"]],
        ["RANGE", [None, 5], ["ADD", [None, 5], [None, 10]]],
        ["LIST", [None, 5], [None, 7], ["ADD", [None, 8], [None, 1]]],
        ["LEN", [None, [0,1,2,3,4]]],
        ["DEREF", [None, 2], [None, ["apple", "banana", "carrot", "dog"]]],
        ["DEREF", [None, "x"], [None, {"x": 5, "y": 7}]],
        ["IS_ZERO", [None, 5]],
        ["IS_ZERO", ["ADD", [None, 3], [None, -3]]],
        ["INCR", [None, 10]],
        ["DECR", [None, 10]],
        ["IF", [None, 1], [None, "if-case"], [None, "else-case"]],
        [
            "IF",
            ["EQ", [None, "x"], [None, "y"]],
            [None, "if-case"],
            [None, "else-case"]
        ],
        ["FACTORIAL", [None, 5]],
        ["MATH_ROW", [None, 7]],
        ["TD", [None, "hello"]],
        ["CONCAT", [None, ["a", "b", "c"]]],
        ["TR", ["LIST", ["TD", [None, "a"]], [None, "<td>b</td>"]]],
        ["APPLY", [[None, "ADD"], [None, 1], [None, 2]]],
        ["MAP", [None, [1, 2, 3]], [None, "DOUBLE"]],
        ["MATH_TR", [None, 7]],
        ["MATH_TABLE_GUTS", ["RANGE", [None, 5], [None, 12]]],
        ["TABLE", [None, "header_row"], [None, ["foo", "bar"]]],
    ]

    for program in programs:
        vm = VirtualMachine(BOTS)

        def callback(answer):
            print '%s ->\n    %s\n' % (program, str(answer))

        vm.process_program(callback, program)

    def write_html(answer):
        open('foo.html', 'w').write(answer)

    vm = VirtualMachine(BOTS)
    vm.process_program(write_html,
        ["MATH_TABLE", ["RANGE", [None, 5], [None, 14]]])

if __name__ == '__main__':
    run()
