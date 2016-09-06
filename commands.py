COMMANDS = [
    ('DOUBLE x',
        '["ADD", [null, x], [null, x]]'),

    ('SQUARE x',
        '["MULT", [null, x], [null, x]]'),

    ('APPLY f',
        ':f ...'),

    ('SPLAT f x',
        ':f *x'),

    ('IS_ZERO x',
        'EQ x 0'),

    ('INCR x',
        'ADD x 1'),

    ('DECR x',
        'ADD x -1'),

    ('TAG tag val',
        'ADD "<" tag ">" (STR val) "</" tag ">"'),

    ('TABLE val',
        'ADD "<table border=1>" val "</table>"'),

    ('TD val',
        'TAG "td" val'),

    ('TR lst',
        '''
        ADD
            (TAG "tr" (SPLAT "ADD" lst))
            "\\n"
        '''),

    ('FACTORIAL x',
        '''
        IF
            (IS_ZERO x)
            1
            (MULT x (FACTORIAL (DECR x)))'''),

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


    ('MATH_ROW n',
        '''
        LIST
            (STR n)
            (DOUBLE n)
            (SQUARE n)
            (FACTORIAL n)
        '''),

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

