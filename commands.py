COMMANDS = [
    ('DOUBLE x',
        ["ADD", {"value": "x"}, {"value": "x"}]),

    ('SQUARE x',
        ["MULT", {"value": "x"}, {"value": "x"}]),

    ('TAG tag val',
        [
            "ADD",
            ["DATA", "<"],
            {"value": "tag"},
            ["DATA", ">"],
            ["STR", {"value": "val"}],
            ["DATA", "</"],
            {"value": "tag"},
            ["DATA", ">"]
        ]),

    ('IS_ZERO x',
        ["EQ", {"value": "x"}, ["DATA", 0]]),

    ('INCR x',
        ["ADD", {"value": "x"}, ["DATA", 1]]),

    ('DECR x',
        ["ADD", {"value": "x"}, ["DATA", -1]]),

    ('FACTORIAL x',
        [
            "IF",
            ["IS_ZERO", {"value": "x"}],
            ["DATA", 1],
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
            ["DATA", ""],
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
        ["CONCAT_SLICE", ["DATA", 0], {"value": "lst"}]),

    ('TR elems',
        [
            "TAG",
            ["DATA", "tr"],
            ["CONCAT", {"value": "elems"}]
        ]),

    ('TD val',
        ["TAG", ["DATA", "td"], {"value": "val"}]),

    ('MAP_SLICE lst index func',
        [
            "IF",
            ["EQ", {"value": "index"}, ["LEN", {"value": "lst"}]],
            ["DATA", []],
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
        ["MAP_SLICE", {"value": "lst"}, ["DATA", 0], {"value": "func"}]),

    ('MATH_TR num',
        [
            "TR",
            [
                "MAP",
                ["MATH_ROW", {"value": "num"}],
                ["DATA", "TD"]
            ]
        ]),

    ('MATH_TABLE_GUTS lst',
        [
            "MAP",
            {"value": "lst"},
            ["DATA", "MATH_TR"]
        ]),

    ('NL str',
        ["ADD", {"value": "str"}, ["DATA", "\n"]]),

    ('TABLE header_row elems',
        [
            "ADD",
            ["DATA", "<table border=1>"],
            ["DATA", "\n"],
            {"value": "header_row"},
            ["DATA", "\n"],
            [
                "CONCAT",
                ["MAP", {"value": "elems"}, ["DATA", "NL"]]
            ],
            ["DATA", "</table>"]
        ]),

    ('MATH_TABLE number_lst',
        [
            "TABLE",
            [
                "TR",
                [
                    "MAP",
                    ["DATA", ["n", "double", "square", "factorial"]],
                    ["DATA", "TD"]
                ]
            ],
            ["MATH_TABLE_GUTS", {"value": "number_lst"}]
        ]),

]

