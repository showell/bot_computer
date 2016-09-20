from bot import BOTS
from vm import VirtualMachine

def run():
    programs = [
        # These are sorted from roughly easiest first to most difficult.
        ["add", ["data", 1], ["data", 2]],
        ["add", ["data", [1, 2]], ["data", [3, 4]]],
        ["double", ["data", 13]],
        ["square", ["add", ["data", 3], ["data", 4]]],
        ["double", ["double", ["data", 5]]],
        ["tag", ["data", "td"], ["data", "hello world"]],
        ["range", ["data", 5], ["add", ["data", 5], ["data", 10]]],
        ["list", ["data", 5], ["data", 7], ["add", ["data", 8], ["data", 1]]],
        ["len", ["data", [0,1,2,3,4]]],
        ["deref", ["data", 2], ["data", ["apple", "banana", "carrot", "dog"]]],
        ["deref", ["data", "x"], ["data", {"x": 5, "y": 7}]],
        ["is_zero", ["data", 5]],
        ["is_zero", ["add", ["data", 3], ["data", -3]]],
        ["incr", ["data", 10]],
        ["decr", ["data", 10]],
        ["if", ["data", 1], ["data", "if-case"], ["data", "else-case"]],
        [
            "if",
            ["eq", ["data", "x"], ["data", "y"]],
            ["data", "if-case"],
            ["data", "else-case"]
        ],
        ["factorial", ["data", 5]],
        ["math_row", ["data", 7]],
        ["td", ["data", "hello"]],
        ["concat", ["data", ["a", "b", "c"]]],
        ["tr", ["list", ["td", ["data", "a"]], ["data", "<td>b</td>"]]],
        ["map", ["data", [1, 2, 3]], ["data", "double"]],
        ["math_tr", ["data", 7]],
        ["math_table_guts", ["range", ["data", 5], ["data", 12]]],
        ["table", ["data", "header_row"], ["data", ["foo", "bar"]]],
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
        ["math_table", ["range", ["data", 5], ["data", 15]]])

if __name__ == '__main__':
    run()
