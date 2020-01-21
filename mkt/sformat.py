"""This modules provides a variety of ways to deal with format."""

import unicodedata
import datetime

def strptime_pre(line, fmt):
    try:
        t = datetime.datetime.strptime(line, fmt)
    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            line = line[:-(len(v.args[0]) - 26)]
            t = datetime.datetime.strptime(line, fmt)
        else:
            raise
    return t

def spacer(length, msg, align=0):
    """
    Parameters
    ----------
    length : length of string in alphabet charcters, Japanese chacters typically takes two alphabet space.
    msg    : string of message to convert.
    align  : 0 - left alined, 1 right alined
    """
    for c in msg:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            length -=2
        else:
            length -=1
    return ' '*length + msg if align else msg + ' '*length
