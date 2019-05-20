import sys

from instapy import set_workspace, Settings
from instapy.database_engine import validate_database_address, create_database


def main():
    username = sys.argv[1]
    workspace_path = sys.argv[2]

    set_workspace(path=workspace_path)

    address = validate_database_address()
    create_database(address, Settings.logger, username)


if __name__== "__main__":
    main()