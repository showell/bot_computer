COMMANDS = [
    ('APPLY f',
        ':f ...'),

    ('SPLAT f x',
        ':f *x'),

    ('DOUBLE x',
        'ADD x x'),

    ('SQUARE x',
        'MULT x x'),

    ('IS_ZERO x',
        'EQ x 0'),

    ('INCR x',
        'ADD x 1'),

    ('DECR x',
        'ADD x -1'),

    ('TAG tag val',
        'ADD "<" tag ">" (STR val) "</" tag ">"'),

    ('TD val',
        'TAG "td" val'),

    ('TR val',
        'TAG "tr" val'),

    ('RANGE x y',
        '''
        IF
            (EQ x y)
            []
            (ADD
                [x]
                (RANGE (INCR x) y))'''),
    ('FACTORIAL x',
        '''
        IF
            (IS_ZERO x)
            1
            (MULT x (FACTORIAL (DECR x)))'''),

    ('MAP_ONE i lst f',
        'APPLY f (DEREF i lst)'),

    ('MAP_REST i lst f',
        '''
        IF
            (EQ i (LEN lst))
            []
            (ADD
                (LIST (MAP_ONE i lst f))
                (MAP_REST (INCR i) lst f))'''),

    ('MAP lst f',
        'MAP_REST 0 lst f'),


    ('MATH_ROW n',
        '''
        LIST
            (DOUBLE n)
            (SQUARE n)
            (FACTORIAL n)
        '''),

    ('MATH_TR n',
        '''
        TR
            (SPLAT
                "ADD"
                (
                    MAP
                        (MATH_ROW n)
                        "TD"
                )
            )
        '''),
]

