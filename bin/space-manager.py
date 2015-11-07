#!/usr/bin/env python

import sys
import os
import subprocess
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def manage_spaces():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='run tests for Building Simulator',
        )
    parser.add_argument(
        '-d',
        '--root-dir',
        default=os.path.join(os.getcwd(), 'sim'),
        help="Recursively search starting at DIR",
        metavar='DIR'
        )
    parser.add_argument(
        '-b',
        '--bin-dir',
        default=os.path.join(os.getcwd(), 'bin'),
        help="Also manage spaces in bin directory found at DIR",
        metavar='DIR'
        )
    parser.add_argument(
        '-s',
        '--tab-width',
        default=4,
        help="Set the NUMBER of spaces a single tab should represent",
        metavar='NUMBER',
        )
    parser.add_argument(
        '-u',
        '--unexpand',
        action='store_true',
        help='Convert spaces back into tabs',
        )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Print a lot of text describing what is happening',
        )
    args = parser.parse_args()

    command = 'expand --initial' if args.unexpand is False else 'unexpand --first-only'
    for root, dirs, files in os.walk(args.root_dir):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                if args.verbose:
                    print("{}ing {}".format(command, file_path))
                try:
                    output = subprocess.check_output(
                        '{} --tabs={} {}'.format(
                            command,
                            args.tab_width,
                            file_path,
                            ),
                        shell=True,
                        stderr=sys.stdout,
                        )
                    if args.verbose:
                        print("{}ed file:".format(command))
                        print(output.decode('utf-8'))
                    with open(file_path, 'wb') as file_handle:
                        file_handle.write(output)
                except subprocess.CalledProcessError as err:
                    print("Failed to expand {}: {}".format(file_name, err))

    for file_name in os.listdir(args.bin_dir):
        file_path = os.path.join(args.bin_dir, file_name)
        with open(file_path, 'r') as file_handle:
            first_line = file_handle.readline().strip()
        if first_line == '#!/usr/bin/env python':
            if args.verbose:
                print("{}ing {}".format(command, file_path))
            try:
                output = subprocess.check_output(
                    '{} --tabs={} {}'.format(
                        command,
                        args.tab_width,
                        file_path,
                        ),
                    shell=True,
                    stderr=sys.stdout,
                    )
                if args.verbose:
                    print("{}ed file:".format(command))
                    print(output.decode('utf-8'))
                with open(file_path, 'wb') as file_handle:
                    file_handle.write(output)
            except subprocess.CalledProcessError as err:
                print("Failed to expand {}: {}".format(file_name, err))

if __name__ == '__main__':
    manage_spaces()
