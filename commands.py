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

    ('TD val',
        '["TAG", [null, "td"], [null, val]]'),

    ###

    ('APPLY f',
        ':f ...'),

    ('SPLAT f x',
        ':f *x'),

    ('TABLE val',
        'ADD "<table border=1>" val "</table>"'),

    ('TR lst',
        '''
        ADD
            (TAG "tr" (SPLAT "ADD" lst))
            "\\n"
        '''),

    ('MAP_SLICE start lst f',
        '''
        IF
            (EQ start (LEN lst))
            []
            (ADD
                (LIST (APPLY f (DEREF start lst)))
                (MAP_SLICE (INCR start) lst f))'''),

    ('MAP lst f',
        'MAP_SLICE 0 lst f'),


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

