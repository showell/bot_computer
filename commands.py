COMMANDS = [
    ('double x',
        ["add", {"value": "x"}, {"value": "x"}]),

    ('square x',
        ["mult", {"value": "x"}, {"value": "x"}]),

    ('tag tag val',
        [
            "add",
            ["data", "<"],
            {"value": "tag"},
            ["data", ">"],
            ["str", {"value": "val"}],
            ["data", "</"],
            {"value": "tag"},
            ["data", ">"]
        ]),

    ('is_zero x',
        ["eq", {"value": "x"}, ["data", 0]]),

    ('incr x',
        ["add", {"value": "x"}, ["data", 1]]),

    ('decr x',
        ["add", {"value": "x"}, ["data", -1]]),

    ('factorial x',
        [
            "if",
            ["is_zero", {"value": "x"}],
            ["data", 1],
            [
                "mult",
                {"value": "x"},
                ["factorial", ["decr", {"value": "x"}]]
            ]
        ]),

    ('math_row val',
        [
            "list",
            ["str", {"value": "val"}],
            ["double", {"value": "val"}],
            ["square", {"value": "val"}],
            ["factorial", {"value": "val"}]
        ]),

    ('concat_slice index lst',
        [
            "if",
            ["eq", {"value": "index"}, ["len", {"value": "lst"}]],
            ["data", ""],
            [
                "add",
                ["deref", {"value": "index"}, {"value": "lst"}],
                [
                    "concat_slice",
                    ["incr", {"value": "index"}],
                    {"value": "lst"}
                ]
            ]
        ]),

    ('concat lst',
        ["concat_slice", ["data", 0], {"value": "lst"}]),

    ('tr elems',
        [
            "tag",
            ["data", "tr"],
            ["concat", {"value": "elems"}]
        ]),

    ('td val',
        ["tag", ["data", "td"], {"value": "val"}]),

    ('map_slice lst index func',
        [
            "if",
            ["eq", {"value": "index"}, ["len", {"value": "lst"}]],
            ["data", []],
            [
                "add",
                [
                    "list",
                    [
                        "apply",
                        [
                            {"value": "func"},
                            ["deref", {"value": "index"}, {"value": "lst"}]
                        ]
                    ]
                ],
                [
                    "map_slice",
                    {"value": "lst"},
                    ["incr", {"value": "index"}],
                    {"value": "func"}
                ]
            ]
        ]),

    ('map lst func',
        ["map_slice", {"value": "lst"}, ["data", 0], {"value": "func"}]),

    ('math_tr num',
        [
            "tr",
            [
                "map",
                ["math_row", {"value": "num"}],
                ["data", "td"]
            ]
        ]),

    ('math_table_guts lst',
        [
            "map",
            {"value": "lst"},
            ["data", "math_tr"]
        ]),

    ('nl str',
        ["add", {"value": "str"}, ["data", "\n"]]),

    ('table header_row elems',
        [
            "add",
            ["data", "<table border=1>"],
            ["data", "\n"],
            {"value": "header_row"},
            ["data", "\n"],
            [
                "concat",
                ["map", {"value": "elems"}, ["data", "nl"]]
            ],
            ["data", "</table>"]
        ]),

    ('math_table number_lst',
        [
            "table",
            [
                "tr",
                [
                    "map",
                    ["data", ["n", "double", "square", "factorial"]],
                    ["data", "td"]
                ]
            ],
            ["math_table_guts", {"value": "number_lst"}]
        ]),

]

