#!/bin/env python3
import subprocess


def main(s: str):
    return subprocess.run(["cat", "dataset/anssi-cible-cc-2020_72en.json"], stdout=subprocess.PIPE).stdout


if __name__ == "__main__":
    print(main())
