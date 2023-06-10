#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Validate or create MicroPython package.json file

MicroPython provides the possiblity to install packages based on a
"package.json" definition file, see
https://docs.micropython.org/en/latest/reference/packages.html#writing-publishing-packages

This script creates such a "package.json" file based on the data specified in
the setup.py file. Additionally the script can validate existing "package.json"
files against the setup.py file and exit with a non zero status in case of a
difference.
"""

import argparse
import json
import logging
from pathlib import Path
from sys import stdout

from .setup2upypackage import Setup2uPyPackage
from .version import __version__


def parser_valid_file(parser: argparse.ArgumentParser, arg: str) -> Path:
    """
    Determine whether file exists.
    :param      parser:                 The parser
    :type       parser:                 parser object
    :param      arg:                    The file to check
    :type       arg:                    str
    :raise      argparse.ArgumentError: Argument is not a file
    :returns:   Input file path, parser error is thrown otherwise.
    :rtype:     Path
    """
    if not Path(arg).is_file():
        parser.error("The file {} does not exist!".format(arg))
    else:
        return Path(arg).resolve()


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    :raise      argparse.ArgumentError  Argparse error
    :return:    argparse object
    """
    parser = argparse.ArgumentParser(description="""
    Validate existing MicroPython package.json file
    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # default arguments
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Output logger messages to stderr')
    parser.add_argument('-v',
                        default=0,
                        action='count',
                        dest='verbosity',
                        help='Set level of verbosity, default is CRITICAL')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {version}'.
                                format(version=__version__),
                        help='Print version of package and exit')

    # specific arguments
    parser.add_argument('--setup_file',
                        dest='setup_file',
                        required=True,
                        type=lambda x: parser_valid_file(parser, x),
                        help='Path to setup.py file')

    parser.add_argument('--package_file',
                        dest='package_file',
                        required=False,
                        type=lambda x: parser_valid_file(parser, x),
                        help='Path to package.json file')

    parser.add_argument('--package_changelog_file',
                        dest='package_changelog_file',
                        required=False,
                        type=lambda x: parser_valid_file(parser, x),
                        help='Path to package changelog file')

    parser.add_argument('--create',
                        dest='dump_to_file',
                        action='store_true',
                        required=False,
                        help='Dump parsed setup.py as package.json to same directory')  # noqa: E501

    parser.add_argument('--validate',
                        dest='do_validate',
                        action='store_true',
                        required=False,
                        help='Validate existing package.json with setup.py based data')  # noqa: E501

    parser.add_argument('--ignore-version',
                        dest='ignore_version',
                        action='store_true',
                        required=False,
                        help='Exclude version from check')

    parser.add_argument('--ignore-deps',
                        dest='ignore_deps',
                        action='store_true',
                        required=False,
                        help='Exclude dependencies from check')

    parser.add_argument('--ignore-boot-main',
                        dest='ignore_boot_main',
                        action='store_true',
                        required=False,
                        help='Boot and main files from check')

    parser.add_argument('--print',
                        dest='print_result',
                        required=False,
                        action='store_true',
                        help='Print parsed setup.py as JSON to stdout')

    parser.add_argument('--pretty',
                        dest='pretty_output',
                        action='store_true',
                        help='Print JSON data at stdout in readable format')

    parsed_args = parser.parse_args()

    return parsed_args


def main():
    # parse CLI arguments
    args = parse_arguments()

    log_levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }
    custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                    ' %(funcName)-15s:%(lineno)4s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=custom_format,
                        stream=stdout)
    logger = logging.getLogger(__name__)
    logger.setLevel(level=log_levels[min(args.verbosity,
                                     max(log_levels.keys()))])
    logger.disabled = not args.debug

    setup_file = args.setup_file
    package_file = args.package_file
    package_changelog_file = args.package_changelog_file
    do_validate = args.do_validate
    dump_to_file = args.dump_to_file
    print_result = args.print_result
    pretty_output = args.pretty_output
    ignore_version = args.ignore_version
    ignore_deps = args.ignore_deps
    ignore_boot_main = args.ignore_boot_main

    setup_2_upy_package = Setup2uPyPackage(
        setup_file=setup_file,
        package_file=package_file,
        package_changelog_file=package_changelog_file,
        logger=logger)

    package_data = setup_2_upy_package.package_data

    if do_validate:
        validation_result = setup_2_upy_package.validate(
            ignore_version=ignore_version,
            ignore_deps=ignore_deps,
            ignore_boot_main=ignore_boot_main)

        if validation_result is False:
            diff = setup_2_upy_package.validation_diff

            if pretty_output:
                stdout.write(json.dumps(diff, indent=4))
            else:
                stdout.write(json.dumps(diff))
            raise SystemExit('Mismatch between setup.py data and package.json')

    if print_result:
        if pretty_output:
            stdout.write(json.dumps(package_data, indent=4))
        else:
            stdout.write(json.dumps(package_data))

    if dump_to_file:
        setup_2_upy_package.create(output_path=package_file,
                                   pretty=pretty_output)


if __name__ == '__main__':
    main()
