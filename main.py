#!/usr/local/bin/python3
import re
import os
import configparser
from argparse import Namespace, ArgumentParser

parser = ArgumentParser(description="Merge contents of folder into one output file")
parser.add_argument(
    "--output",
    type=str,
    help='Output file location ("codingame.volatile.py" be ' "default)",
)
parser.add_argument(
    "--workdir",
    type=str,
    help="Folder that will be searched for files to merge in output file",
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
    "--comment", type=str, help='Comment character ("#" by default)',
)
parser.add_argument(
    "--separator-start",
    type=str,
    help="Character appended to comment "
    'indicating start of file contents ("-" by '
    "default)",
)
parser.add_argument(
    "--separator-end",
    type=str,
    help="Character appended to comment "
    'indicating end of file contents ("=" by '
    "default)",
)
parser.add_argument(
    "--separator-length",
    type=str,
    help="how many characters to left-pad to indicate contents from other files (80 "
    "by default)",
)
parser.add_argument(
    "--file-regex",
    type=str,
    help="pythonic regex used to filter-out files in "
    'workdir (".*" by default - it will process all of the files in the workdir '
    "folder)",
)
parser.add_argument(
    "--exclude-line-regex",
    type=str,
    help="pythonic regex used to filter-out lines of files that would cause a mess "
    'during the merge ("^from codingame\.|^import codingame|^from \.|^import \." by '
    "default to exclude python local imports)",
)
parser.add_argument("--debug", action="store_true", help="print current settings")
parser.add_argument(
    "--write",
    action="store_true",
    help="Write current settings in form of a file ("
    "they will be used instead of the command "
    "line settings)",
)

config = configparser.ConfigParser(
    defaults={
        "output": "codingame.volatile.py",
        "workdir": "codingame/",
        "main": "main.py",
        "file_regex": ".*",
        "exclude_line_regex": "^from codingame\.|^import codingame|^from \.|^import \.",
        "comment": "#",
        "separator_start": "-",
        "separator_end": "=",
        "separator_length": "80",
    },
    default_section="merger",
)


def in_workdir(file_name: str):
    return os.path.isdir(os.path.join(config["merger"]["workdir"], file_name))


def check_output_exists():
    if not os.path.exists(config["merger"]["output"]):
        parser.error(
            f"No \"{config['merger']['output']}\" file present in {os.getcwd()}"
        )


def check_header_exists():
    if not os.path.exists(config["merger"]["header"]):
        parser.error(
            f"No \"{config['merger']['header']}\" file present in {os.getcwd()}"
        )


def check_workdir_exists():
    if not os.path.isdir(config["merger"]["workdir"]):
        parser.error(
            f"No \"{config['merger']['workdir']}\" directory present in {os.getcwd()}"
        )


def check_is_in_workdir(file_name: str):
    if not in_workdir(file_name):
        parser.error(
            f'No "{file_name}" directory present in {os.getcwd()}'
            f'/{config["merger"]["workdir"]}',
        )


def write_to_output_file(file_name, current_file, output_file, exclude_line_regex):
    start_file_comment = f'{config["merger"]["comment"]} file "{file_name}" '.ljust(
        int(config["merger"]["separator_length"]),
        config["merger"]["separator_start"][0],
    )
    output_file.write(f"\n{start_file_comment}\n")
    for line in current_file.readlines():
        if not exclude_line_regex.search(line):
            output_file.write(line)

    end_file_comment = (
        f'{config["merger"]["comment"]} end of file "{file_name}" '
        f"".ljust(
            int(config["merger"]["separator_length"]),
            config["merger"]["separator_end"][0],
        )
    )
    output_file.write(f"\n\n\n{end_file_comment}\n")


def log_values():
    print("")
    print("output: ", config["merger"].get("output", "none"))
    print("workdir: ", config["merger"].get("workdir", "none"))
    print("main: ", config["merger"].get("main", "none"))
    print("file_regex: ", config["merger"].get("file_regex", "none"))
    print("exclude_line_regex: ", config["merger"].get("exclude_line_regex", "none"))
    print("header: ", config["merger"].get("header", "none"))
    print("comment: ", config["merger"].get("comment", "none"))
    print("separator_start: ", config["merger"].get("separator_start", "none"))
    print("separator_end: ", config["merger"].get("separator_end", "none"))
    print("separator_length: ", config["merger"].get("separator_length", "none"))
    print("")


def main(arguments: Namespace):
    if os.path.exists("cgmerger.conf"):
        config.read("cgmerger.conf")
    else:
        print("")
        print(
            "No cgmerger.conf file found. The script will run with default "
            "settings. run the command with --write flag to write new cgmerger.conf "
            "file or override the current one. Run the command with --debug flag to "
            "check the current settings"
        )
        print("")

    if arguments.file_regex is not None:
        config["merger"]["file_regex"] = arguments.file_regex
    if arguments.exclude_line_regex is not None:
        config["merger"]["exclude_line_regex"] = arguments.exclude_line_regex
    if arguments.output is not None:
        config["merger"]["output"] = arguments.output
    if arguments.workdir is not None:
        config["merger"]["workdir"] = arguments.workdir
    if arguments.main is not None:
        config["merger"]["main"] = arguments.main
    if arguments.header is not None:
        config["merger"]["header"] = arguments.header
    if arguments.comment is not None:
        config["merger"]["comment"] = arguments.comment

    if arguments.debug:
        log_values()
        parser.exit(message="No further operations will be performed")

    if arguments.write:
        with open("cgmerger.conf", "w") as config_file:
            config.write(config_file)
        log_values()
        parser.exit(message="Config file created with listed values")

    check_output_exists()

    check_workdir_exists()

    order = None
    output_file_location = config["merger"]["output"]
    main_file = config["merger"]["main"]
    work_dir = config["merger"]["workdir"]
    file_regex = re.compile(config["merger"]["file_regex"])
    exclude_line_regex = re.compile(config["merger"]["exclude_line_regex"])
    header_file = None

    if "header" in config["merger"]:
        header_file = config["merger"]["header"]

    if "order" in config["merger"]:
        order = config["merger"]["order"].split(",")

    if order is not None:
        for file_name in order:
            check_is_in_workdir(file_name)

    if header_file is not None:
        check_header_exists()

    files_to_watch = [
        f for f in os.listdir(work_dir) if os.path.isfile(os.path.join(work_dir, f))
    ]

    with open(output_file_location, "w") as output_file:
        # all of the files, which are not in main, are are not in order
        if header_file is not None:
            with open(header_file, "r") as current_file:
                write_to_output_file(
                    header_file, current_file, output_file, exclude_line_regex
                )

        for f in files_to_watch:
            if f == main_file:
                continue

            if order is not None and f in order:
                continue

            if not file_regex.search(f):
                continue

            with open(os.path.join(work_dir, f), "r") as current_file:
                write_to_output_file(f, current_file, output_file, exclude_line_regex)

        # now files that should go in order
        if order is not None:
            for f in order:
                if f == main_file:
                    continue

                with open(os.path.join(work_dir, f), "r") as current_file:
                    write_to_output_file(
                        f, current_file, output_file, exclude_line_regex
                    )

        # Main will always be the last one
        with open(os.path.join(work_dir, main_file), "r") as current_file:
            write_to_output_file(
                main_file, current_file, output_file, exclude_line_regex
            )


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
