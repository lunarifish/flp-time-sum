"""
This script is used to parse flp files and sum up the working time.
"""

import os
import sys
import datetime

from typing import Union, NoReturn

import pyflp
from tqdm import tqdm


def validate_path(path: str) -> Union[str, NoReturn]:
    if not os.path.isdir(path):
        print(f"Invalid path: {path}")
        sys.exit(1)
    return path


if __name__ == "__main__":

    ## get paths from console input

    if len(sys.argv) > 1:
        DIRS = [validate_path(path) for path in sys.argv[1:]]
    else:
        print("usage: python main.py <path1> <path2> ...")
        sys.exit(1)

    ####

    ## Get path to all flp files in the given directory

    project_files = list()

    for directory in DIRS:
        project_files += [os.path.join(root, file) for (root, dirs, files)
                          in os.walk(directory) for file in files if file.endswith(".flp")]

    if project_files:
        print(f"Found {len(project_files)} flp files")
    else:
        print(f"No flp files found in {DIRS}")
        sys.exit(0)

    ####

    ## Parse the project files and sum up working time

    working_time_sum = datetime.timedelta()
    failed_count = 0

    for project_file in tqdm(project_files):
        try:
            project = pyflp.parse(project_file)
            working_time_sum += project.time_spent
        except Exception as e:
            failed_count += 1
            print(f"\n{project_file} failed to parse")

    ####

    print("\n" + "-" * 40)
    print(f"Total {len(project_files)} files, success: {len(project_files) - failed_count}, failed: {failed_count}")
    print(f"Total working time = {working_time_sum}")
    print((" " * 18) + f" = {working_time_sum.total_seconds() / 3600:.2f} hours")
