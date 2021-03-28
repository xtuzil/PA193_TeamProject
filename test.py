#!/bin/env python3
from output_compare import check_title, check_versions, check_toc, check_revisions, check_bibliography, load_file
from typing import List, Tuple
from math import ceil
import glob
import json
import certificate_parser


def test_file(filename: str, result: List[int]):
    actual = json.loads(certificate_parser.main(filename + ".txt"))
    expected = load_file(filename + ".json")

    checks = (check_title, check_versions, check_toc, check_revisions, check_bibliography)
    for check in checks:
        try:
            result.append(ceil(check(actual, expected)))
        except Exception:
            result.append(-20)


def print_result(result: Tuple[str, List[int], int]):
    print(result[0][:40].ljust(40), end="")
    for num in result[1]:
        print(str(num).rjust(3), end=" ")
    print("| " + str(result[2]).rjust(3))


def main():
    files = glob.glob("dataset/*.txt")
    files = [file.rsplit('.', 1)[0] for file in files]
    results = []
    print("Filename".ljust(40) + "Tit Ver ToC Rev Bib | Sum")
    for file in files:
        test_result = []
        test_file(file, test_result)
        file = file.split('/', 1)[1]
        results.append((file, test_result, sum(test_result)))

    for result in results:
        print_result(result)
    results.sort(key=lambda item: item[2])
    print("\n5 Worst:")
    for i in range(5):
        print_result(results[i])
    print("\nOverall score: " + str(sum([x[2] for x in results])) + " / " + str(len(results)*len(results[0][1])*20))


if __name__ == '__main__':
    main()
