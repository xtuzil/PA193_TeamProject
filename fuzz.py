#!/bin/env python3
import ntpath
import os
from pathlib import Path
import random
import pyradamsa
from Certificate import Certificate
import glob
import parse


def test(filename: Path):
    try:
        with open(filename, 'r') as file:
            parse.main([Certificate(str(filename), file.read())])
        Path.unlink(Path("./output/" + str(filename.stem) + ".json"))
        Path.unlink(filename)
    except UnicodeDecodeError:
        Path.unlink(filename)
    # except FileNotFoundError as e:
    #     print("Not found: " + str(e.filename))
    except Exception as e:
        print(str(filename) + " failed with " + str(e))


def main():
    files = glob.glob("dataset/*.txt")
    rad = pyradamsa.Radamsa()
    if not os.path.exists("input"):
        os.makedirs("input")
    i = 0
    while True:
        base_filename = Path(random.choice(files))
        fuzzed_filename = Path("./input/" + str(i) + "_" + ntpath.basename(base_filename))
        with open(base_filename, 'r') as file:
            fuzzed = rad.fuzz(bytes(file.read(), "utf-8"))
        with open(fuzzed_filename, "wb") as file:
            file.write(fuzzed)
        test(fuzzed_filename)
        i += 1


if __name__ == '__main__':
    main()
