COMMANDS = [
    ('DOUBLE x',
        '["ADD", [null, x], [null, x]]'),

    ('SQUARE x',
        '["MULT", [null, x], [null, x]]'),

    ('TAG tag val',
        '''
        [
            "ADD",
            [null, "<"],
            [null, tag],
            [null, ">"],
            ["STR", [null, val]],
            [null, "</"],
            [null, tag],
            [null, ">"]
        ]
        '''),

    ('IS_ZERO x',
        '["EQ", [null, x], [null, 0]]'),

    ('INCR x',
        '["ADD", [null, x], [null, 1]]'),

    ('DECR x',
        '["ADD", [null, x], [null, -1]]'),

    ('FACTORIAL x',
        '''
        [
            "IF",
            ["IS_ZERO", [null, x]],
            [null, 1],
            [
                "MULT",
                [null, x],
                ["FACTORIAL", ["DECR", [null, x]]]
            ]
        ]
        '''),

    ('MATH_ROW val',
        '''
        [
            "LIST",
            ["STR", [null, val]],
            ["DOUBLE", [null, val]],
            ["SQUARE", [null, val]],
            ["FACTORIAL", [null, val]]
        ]
        '''),

    ('CONCAT_SLICE index lst',
        '''
        [
            "IF",
            ["EQ", [null, index], ["LEN", [null, lst]]],
            [null, ""],
            [
                "ADD",
                ["DEREF", [null, index], [null, lst]],
                [
                    "CONCAT_SLICE",
                    ["INCR", [null, index]],
                    [null, lst]
                ]
            ]
        ]
        '''),

    ('CONCAT lst',
        '["CONCAT_SLICE", [null, 0], [null, lst]]'),

    ('TR elems',
        '''
        [
            "TAG",
            [null, "tr"],
            ["CONCAT", [null, elems]]
        ]
        '''),

    ('TD val',
        '["TAG", [null, "td"], [null, val]]'),

    ('MAP_SLICE lst index func',
        '''
        [
            "IF",
            ["EQ", [null, index], ["LEN", [null, lst]]],
            [null, []],
            [
                "ADD",
                [
                    "LIST",
                    [
                        "APPLY",
                        [
                            func,
                            ["DEREF", [null, index], [null, lst]]
                        ]
                    ]
                ],
                [
                    "MAP_SLICE",
                    [null, lst],
                    ["INCR", [null, index]],
                    [null, func]
                ]
            ]
        ]
        '''),

    ('MAP lst func',
        '["MAP_SLICE", [null, lst], [null, 0], [null, func]]'),

    ('MATH_TR num',
        '''
        [
            "TR",
            [
                "MAP",
                ["MATH_ROW", [null, num]],
                [null, "TD"]
            ]
        ]
        '''),

    ('MATH_TABLE_GUTS lst',
        '''
        [
            "MAP",
            [null, lst],
            [null, "MATH_TR"]
        ]
        '''),

    ('NL str',
        '["ADD", [null, str], [null, "\\n"]]'),

    ('TABLE header_row elems',
        '''
        [
            "ADD",
            [null, "<table border=1>"],
            [null, "\\n"],
            [null, header_row],
            [null, "\\n"],
            [
                "CONCAT",
                ["MAP", [null, elems], [null, "NL"]]
            ],
            [null, "</table>"]
        ]
        '''),

    ('MATH_TABLE number_lst',
        '''
        [
            "TABLE",
            [
                "TR",
                [
                    "MAP",
                    [null, ["n", "double", "square", "factorial"]],
                    [null, "TD"]
                ]
            ],
            ["MATH_TABLE_GUTS", [null, number_lst]]
        ]
        '''),

]

