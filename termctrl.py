from atexit import register
from sys import stdout
CSI = '\x1b['
def write(str):
    home()
    stdout.write(str)
def control(str):
    stdout.write(CSI+str)
    stdout.flush()
def erase():
    control('2K')
def home():
    control('G')
def priorline():
    control('A')
def hide():
    control('?25l')
def show():
    control('?25h')
if meter:
    hide()
    register(show)
