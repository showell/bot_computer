from bot import BOTS
from vm import VirtualMachine

def run():
    programs = [
        # These are sorted from roughly easiest first to most difficult.
        ["ADD", ["DATA", 1], ["DATA", 2]],
        ["ADD", ["DATA", [1, 2]], ["DATA", [3, 4]]],
        ["DOUBLE", ["DATA", 13]],
        ["SQUARE", ["ADD", ["DATA", 3], ["DATA", 4]]],
        ["DOUBLE", ["DOUBLE", ["DATA", 5]]],
        ["TAG", ["DATA", "td"], ["DATA", "hello world"]],
        ["RANGE", ["DATA", 5], ["ADD", ["DATA", 5], ["DATA", 10]]],
        ["LIST", ["DATA", 5], ["DATA", 7], ["ADD", ["DATA", 8], ["DATA", 1]]],
        ["LEN", ["DATA", [0,1,2,3,4]]],
        ["DEREF", ["DATA", 2], ["DATA", ["apple", "banana", "carrot", "dog"]]],
        ["DEREF", ["DATA", "x"], ["DATA", {"x": 5, "y": 7}]],
        ["IS_ZERO", ["DATA", 5]],
        ["IS_ZERO", ["ADD", ["DATA", 3], ["DATA", -3]]],
        ["INCR", ["DATA", 10]],
        ["DECR", ["DATA", 10]],
        ["IF", ["DATA", 1], ["DATA", "if-case"], ["DATA", "else-case"]],
        [
            "IF",
            ["EQ", ["DATA", "x"], ["DATA", "y"]],
            ["DATA", "if-case"],
            ["DATA", "else-case"]
        ],
        ["FACTORIAL", ["DATA", 5]],
        ["MATH_ROW", ["DATA", 7]],
        ["TD", ["DATA", "hello"]],
        ["CONCAT", ["DATA", ["a", "b", "c"]]],
        ["TR", ["LIST", ["TD", ["DATA", "a"]], ["DATA", "<td>b</td>"]]],
        ["APPLY", [["DATA", "ADD"], ["DATA", 1], ["DATA", 2]]],
        ["MAP", ["DATA", [1, 2, 3]], ["DATA", "DOUBLE"]],
        ["MATH_TR", ["DATA", 7]],
        ["MATH_TABLE_GUTS", ["RANGE", ["DATA", 5], ["DATA", 12]]],
        ["TABLE", ["DATA", "header_row"], ["DATA", ["foo", "bar"]]],
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
        ["MATH_TABLE", ["RANGE", ["DATA", 5], ["DATA", 15]]])

if __name__ == '__main__':
    run()
