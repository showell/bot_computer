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

    ###

    ('SPLAT f x',
        ':f *x'),

    ('TABLE val',
        'ADD "<table border=1>" val "</table>"'),

    ('MATH_TR n',
        '''
        TR (
            MAP
                (MATH_ROW n)
                "TD"
        )
        '''),
    ('MATH_TABLE n',
        '''
        TABLE (
            ADD
            (TR (MAP ["i", "2*i", "i**2", "i!"] "TD"))
            (SPLAT "ADD" (
                MAP
                    (RANGE 0 n)
                    "MATH_TR"
                )
            )
        )
        '''),
]

