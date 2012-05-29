from __future__ import print_function

from datetime import datetime
import sys

from clint.textui import colored

def yield_colorers():
    for color in ('cyan', 'yellow', 'green', 'magenta', 'red'):
        yield getattr(colored, color)
    while True:
        yield lambda x: x

def write_message(message, tag, colorer=lambda x:x):
    for line in message.splitlines():
        formatted = colorer('%s %-13s | ' % (datetime.now().strftime('%H:%M:%S'), tag)) + line
        print(formatted, file=sys.stderr)
