#!/bin/env python3
import ntpath
import os
import random

import pyradamsa

from Certificate import Certificate
import glob
import parse


def test(filename: str):
    try:
        with open(filename, 'r') as file:
            parse.main([Certificate(filename, file.read())])
        os.remove("./output/" + ntpath.splitext(ntpath.basename(filename))[0] + ".json")
        os.remove(filename)
    except UnicodeDecodeError:
        os.remove(filename)
    # except FileNotFoundError as e:
    #     print("Not found: " + str(e.filename))
    except Exception as e:
        print(filename + " failed with " + str(e))


def main():
    files = glob.glob("dataset/*.txt")
    rad = pyradamsa.Radamsa()
    if not os.path.exists("input"):
        os.makedirs("input")
    i = 0
    while True:
        base_filename = random.choice(files)
        fuzzed_filename = "./input/" + str(i) + "_" + ntpath.basename(base_filename)
        with open(base_filename, 'r') as file:
            fuzzed = rad.fuzz(bytes(file.read(), "utf-8"))
        with open(fuzzed_filename, "wb") as file:
            file.write(fuzzed)
        test(fuzzed_filename)
        i += 1


if __name__ == '__main__':
    main()
