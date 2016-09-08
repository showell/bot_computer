COMMANDS = [
    ('DOUBLE x',
        ["ADD", {"value": "x"}, {"value": "x"}]),

    ('SQUARE x',
        ["MULT", {"value": "x"}, {"value": "x"}]),

    ('TAG tag val',
        [
            "ADD",
            [None, "<"],
            {"value": "tag"},
            [None, ">"],
            ["STR", {"value": "val"}],
            [None, "</"],
            {"value": "tag"},
            [None, ">"]
        ]),

    ('IS_ZERO x',
        ["EQ", {"value": "x"}, [None, 0]]),

    ('INCR x',
        ["ADD", {"value": "x"}, [None, 1]]),

    ('DECR x',
        ["ADD", {"value": "x"}, [None, -1]]),

    ('FACTORIAL x',
        [
            "IF",
            ["IS_ZERO", {"value": "x"}],
            [None, 1],
            [
                "MULT",
                {"value": "x"},
                ["FACTORIAL", ["DECR", {"value": "x"}]]
            ]
        ]),

    ('MATH_ROW val',
        [
            "LIST",
            ["STR", {"value": "val"}],
            ["DOUBLE", {"value": "val"}],
            ["SQUARE", {"value": "val"}],
            ["FACTORIAL", {"value": "val"}]
        ]),

    ('CONCAT_SLICE index lst',
        [
            "IF",
            ["EQ", {"value": "index"}, ["LEN", {"value": "lst"}]],
            [None, ""],
            [
                "ADD",
                ["DEREF", {"value": "index"}, {"value": "lst"}],
                [
                    "CONCAT_SLICE",
                    ["INCR", {"value": "index"}],
                    {"value": "lst"}
                ]
            ]
        ]),

    ('CONCAT lst',
        ["CONCAT_SLICE", [None, 0], {"value": "lst"}]),

    ('TR elems',
        [
            "TAG",
            [None, "tr"],
            ["CONCAT", {"value": "elems"}]
        ]),

    ('TD val',
        ["TAG", [None, "td"], {"value": "val"}]),

    ('MAP_SLICE lst index func',
        [
            "IF",
            ["EQ", {"value": "index"}, ["LEN", {"value": "lst"}]],
            [None, []],
            [
                "ADD",
                [
                    "LIST",
                    [
                        "APPLY",
                        [
                            {"value": "func"},
                            ["DEREF", {"value": "index"}, {"value": "lst"}]
                        ]
                    ]
                ],
                [
                    "MAP_SLICE",
                    {"value": "lst"},
                    ["INCR", {"value": "index"}],
                    {"value": "func"}
                ]
            ]
        ]),

    ('MAP lst func',
        ["MAP_SLICE", {"value": "lst"}, [None, 0], {"value": "func"}]),

    ('MATH_TR num',
        [
            "TR",
            [
                "MAP",
                ["MATH_ROW", {"value": "num"}],
                [None, "TD"]
            ]
        ]),

    ('MATH_TABLE_GUTS lst',
        [
            "MAP",
            {"value": "lst"},
            [None, "MATH_TR"]
        ]),

    ('NL str',
        ["ADD", {"value": "str"}, [None, "\n"]]),

    ('TABLE header_row elems',
        [
            "ADD",
            [None, "<table border=1>"],
            [None, "\n"],
            {"value": "header_row"},
            [None, "\n"],
            [
                "CONCAT",
                ["MAP", {"value": "elems"}, [None, "NL"]]
            ],
            [None, "</table>"]
        ]),

    ('MATH_TABLE number_lst',
        [
            "TABLE",
            [
                "TR",
                [
                    "MAP",
                    [None, ["n", "double", "square", "factorial"]],
                    [None, "TD"]
                ]
            ],
            ["MATH_TABLE_GUTS", {"value": "number_lst"}]
        ]),

]

