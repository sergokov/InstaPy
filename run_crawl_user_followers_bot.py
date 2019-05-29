
import sys
import sqlite3

from instapy import InstaPy, Settings
from instapy import smart_run
from instapy import set_workspace


def main():
    # login credentials
    insta_username = sys.argv[1]
    insta_password = sys.argv[2]
    target_profile = sys.argv[3]
    workspace_path = sys.argv[4]

    set_workspace(path=workspace_path)

    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      disable_image_load=True,
                      multi_logs=True)

    with smart_run(session):
        followers = session.grab_followers(username=target_profile, amount="full", live_match=True, store_locally=True)
        print(followers)

    for follower in followers:
        insert_follower(target_profile, follower)


def insert_follower(profile_name, name):
    query = "INSERT INTO follower (profile_name, name) VALUES ('{}', '{}');"\
        .format(profile_name, name)

    connection = sqlite3.connect(Settings.database_location)
    with connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)


if __name__== "__main__":
    main()