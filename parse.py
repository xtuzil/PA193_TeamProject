import argparse
import errno
import os
from typing import Optional, List

from Certificate import Certificate
from Enum.JsonStructureKeys import JsonStructureKey
from ParsingModules.ParsingModulesContainer import ParsingModulesContainer


def main(
        certificates: List[Certificate],
        pretty_print: Optional[List[JsonStructureKey]] = None,
        out_dir: str = 'output') -> None:
    if not out_dir.endswith("/"):
        out_dir = out_dir + "/"

    # iterate over certificates
    for certificate in certificates:
        for parsing_module in ParsingModulesContainer.get_parsing_modules(pretty_print):
            # give certificate to modules so each parse its part
            parsing_module.parse(certificate)

        # create file if does not exist
        output_filename = out_dir + certificate.get_json_filename()
        if not os.path.exists(os.path.dirname(output_filename)):
            try:
                os.makedirs(os.path.dirname(output_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # output json to file
        with open(output_filename, "w") as out_file:
            out_file.write(certificate.to_json(pretty_print))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse certificates to json')
    parser.add_argument('files', metavar='N', type=open, nargs='+', help='Files')
    parser.add_argument('--pretty-print', '-p', nargs='*', choices=JsonStructureKey.get_values(), help='Pretty print')
    parser.add_argument('--output-dir', '-o', type=str, help='Output directory', default="output")
    parser.add_help = True

    try:
        args = parser.parse_args()
        arg_certificates = []
        for file in args.files:
            # transform file to Certificate class
            arg_certificates.append(Certificate(file.name, file.read()))

        main(arg_certificates, args.pretty_print, args.output_dir)

    except FileNotFoundError as not_found:
        print("File " + str(not_found.filename) + " not found")
        exit(1)
    except UnicodeDecodeError as decode_err:
        print("File " + file.name + " has invalid format: " + str(decode_err))
        exit(2)
