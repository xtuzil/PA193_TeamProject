#!/bin/env python3
from Certificate import Certificate
from output_compare import check_title, check_versions, check_toc, check_revisions, check_bibliography, load_file
from typing import List, Tuple
from math import ceil
import glob
import parse


def test_file(filename: str, result: List[int]):
    actual = load_file("output/" + filename)
    expected = load_file("dataset/" + filename)

    checks = [check_title, check_versions, check_toc, check_revisions, check_bibliography]
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
    certificates = []
    for filename in files:
        with open(filename, 'r') as file:
            certificates.append(Certificate(filename, file.read()))
    parse.main(certificates)
    test_results = []
    print("Filename".ljust(40) + "Tit Ver ToC Rev Bib | Sum")
    for cert in certificates:
        test_result = []
        test_file(cert.get_filename()[:-4] + ".json", test_result)
        test_results.append((cert.get_filename(), test_result, sum(test_result)))

    for result in test_results:
        print_result(result)
    test_results.sort(key=lambda item: item[2])
    print("\n10 Worst:")
    for i in range(10):
        print_result(test_results[i])
    print("\nOverall score: " + str(sum([x[2] for x in test_results])) + " / "
          + str(len(test_results)*len(test_results[0][1])*20))
    print("\nAdjusted score: " + str(sum([x[2] for x in test_results[5:]])) + " / "
          + str(len(test_results[5:]) * len(test_results[0][1]) * 20))


if __name__ == '__main__':
    main()
