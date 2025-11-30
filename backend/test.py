import os, pathlib


print(pathlib.Path(__file__).stem)

def do_sth():
    print(do_sth.__name__)

do_sth()