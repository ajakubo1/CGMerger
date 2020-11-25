#!/usr/local/bin/python3
import re
import os
import configparser
import argparse
from argparse import Namespace

parser = argparse.ArgumentParser(
    description="Merge contents of folder into one " "output file"
)
parser.add_argument(
    "--output", type=str, help="Output file location", default="program.volatile.py"
)
parser.add_argument(
    "--workdir",
    type=str,
    help="Folder that will be searched for " "files to merge in output file",
)
parser.add_argument(
    "--main",
    type=str,
    help="main file in workdir that will be copied the last (main loop should be "
    "placed in here)",
)
parser.add_argument(
    "--header",
    type=str,
    help="File from which the top part of output file will be copied (you should put "
    "all of the imports/using/includes here depending on your language)",
)
parser.add_argument(
    "--file-regex", type=str, help="regex used to filter-out files in workdir",
)
parser.add_argument("--debug", action="store_true", help="print current settings")
parser.add_argument(
    "--write", action="store_true", help="Write current settings in form of a file"
)

config = configparser.ConfigParser(
    defaults={
        "output": "program.volatile.py",
        "workdir": "program",
        "main": "main.py",
        "file_regex": ".*",
    },
    default_section="merger",
)


def in_workdir(file_name: str):
    return os.path.isdir(os.path.join(config["merger"]["workdir"], file_name))


def check_output_exists():
    if not os.path.exists(config["merger"]["output"]):
        raise Exception(
            f"No \"{config['merger']['output']}\" file present in {os.getcwd()}"
        )


def check_header_exists():
    if not os.path.exists(config["merger"]["header"]):
        raise Exception(
            f"No \"{config['merger']['header']}\" file present in {os.getcwd()}"
        )


def check_workdir_exists():
    if not os.path.isdir(config["merger"]["workdir"]):
        raise Exception(
            f"No \"{config['merger']['workdir']}\" directory present in {os.getcwd()}"
        )


def check_is_in_workdir(file_name: str):
    if not in_workdir(file_name):
        raise Exception(
            f'No "{file_name}" directory present in {os.getcwd()}'
            f'/{config["merger"]["workdir"]}',
        )


def write_to_output_file(file_name, current_file, output_file, work_dir):
    output_file.write(
        f'\n# file "{file_name}" ' f"----------------------------------\n"
    )
    for line in current_file.readlines():
        if (
            not line.startswith("from .")
            and not line.startswith(f"from {work_dir}")
            and not line.startswith(f"import {work_dir}")
            and not line.startswith("import .")
        ):
            output_file.write(line)
    output_file.write(
        f'\n\n\n# endof "{file_name} ' f'================================="\n'
    )


def main(arguments: Namespace):
    if os.path.exists("cgmerger.conf"):
        config.read("cgmerger.conf")
    else:
        print(
            "No cgmerger.conf file found. The script will run with default "
            "settings. run the command with --write flat to write new cgmerger.conf "
            "file or override the current one. Run the command with --debug flag to "
            "check the current settings"
        )

    if arguments.file_regex is not None:
        config["merger"]["file_regex"] = arguments.file_regex
    if arguments.output is not None:
        config["merger"]["output"] = arguments.output
    if arguments.workdir is not None:
        config["merger"]["workdir"] = arguments.workdir
    if arguments.main is not None:
        config["merger"]["main"] = arguments.main
    if arguments.header is not None:
        config["merger"]["header"] = arguments.header

    if arguments.debug:
        print("file_regex: ", config["merger"].get("file_regex", "none"))
        print("output: ", config["merger"].get("output", "none"))
        print("workdir: ", config["merger"].get("workdir", "none"))
        print("main: ", config["merger"].get("main", "none"))
        print("header: ", config["merger"].get("header", "none"))
        print("")
        print("No other operations will be performed")
        return

    if arguments.write:
        with open("cgmerger.conf", "w") as config_file:
            config.write(config_file)
        return

    try:
        check_output_exists()
    except Exception as e:
        print(e)
        return

    try:
        check_workdir_exists()
    except Exception as e:
        print(e)
        return

    order = None
    output_file_location = config["merger"]["output"]
    main_file = config["merger"]["main"]
    work_dir = config["merger"]["workdir"]
    file_regex = re.compile(config["merger"]["file_regex"])
    header_file = None

    if "header" in config["merger"]:
        header_file = config["merger"]["header"]

    if "order" in config["merger"]:
        order = config["merger"]["order"].split(",")

    if order is not None:
        for file_name in order:
            try:
                check_is_in_workdir(file_name)
            except Exception as e:
                print(e)
                return

    if header_file is not None:
        try:
            check_header_exists()
        except Exception as e:
            print(e)
            return

    files_to_watch = [
        f for f in os.listdir(work_dir) if os.path.isfile(os.path.join(work_dir, f))
    ]

    with open(output_file_location, "w") as output_file:
        # all of the files, which are not in main, are are not in order
        if header_file is not None:
            with open(header_file, "r") as current_file:
                write_to_output_file(header_file, current_file, output_file, work_dir)

        for f in files_to_watch:
            if f == main_file:
                continue

            if order is not None and f in order:
                continue

            if not file_regex.search(f):
                continue

            with open(os.path.join(work_dir, f), "r") as current_file:
                write_to_output_file(f, current_file, output_file, work_dir)

        # now files that should go in order
        if order is not None:
            for f in order:
                if f == main_file:
                    continue

                with open(os.path.join(work_dir, f), "r") as current_file:
                    write_to_output_file(f, current_file, output_file, work_dir)

        # Main will always be the last one
        with open(os.path.join(work_dir, main_file), "r") as current_file:
            write_to_output_file(main_file, current_file, output_file, work_dir)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
