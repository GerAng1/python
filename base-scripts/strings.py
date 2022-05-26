"""Some of the many things you can do with strings.
Try to use them to be more pythonic.
"""

love_maybe_lines = [
    'Always    ',
    '     in the middle of our bloodiest battles  ',
    'you lay down your arms',
    '           like flowering mines    ',
    '\n',
    '   to conquer me home.    '
    ]

love_maybe_lines_stripped = [i.strip() for i in love_maybe_lines]

love_maybe_full = '\n'.join(love_maybe_lines_stripped)
print(love_maybe_full)
