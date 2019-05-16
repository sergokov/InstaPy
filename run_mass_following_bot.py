import random
import sys
import sqlite3

from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace
from instapy.database_engine import get_database


def main():
    # set_workspace(path="/home/pi/IG/Workspace")
    set_workspace(path="/home/sergo/InstaPy")

    # login credentials
    insta_username = sys.argv[1]
    insta_password = 'password'
    # insta_password = sys.argv[2]
    # target_profile = sys.argv[3]
    # users_num = sys.argv[4]
    # crawler_db_path = sys.argv[5]

    users = ['shampoo_rnd', 'nurdielemes', 'aleksei.pronin19', '_olenka_0806', 'xx1', 'xx2', 'xx3']


    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      disable_image_load=True,
                      multi_logs=True)

    target_users = find_users_not_interacted(users)

    with smart_run(session):
        session.set_simulation(enabled=True, percentage=80)
        session.set_action_delays(enabled=True,
                                  like=5,
                                  follow=7,
                                  unfollow=28,
                                  random_range=(70, 130))

        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=None,
                                        delimit_by_numbers=True,
                                        max_followers=3000,
                                        max_following=1000,
                                        min_followers=5,
                                        min_following=5)

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "follows", "unfollows", "server_calls_h"],
                                     sleepyhead=True,
                                     stochastic_flow=True,
                                     notify_me=True,
                                     peak_likes=(32, 110),
                                     peak_follows=(31, 110),
                                     peak_unfollows=(35, 120),
                                     peak_server_calls=(1000, 3000))

        session.set_user_interact(amount=4, randomize=True, percentage=90, media='Photo')
        session.set_do_like(enabled=True, percentage=80)
        session.set_do_follow(enabled=True, percentage=20, times=1)

        # activities
        session.follow_by_list(target_users, 1, sleep_delay=600, interact=True)

        session.unfollow_users(amount=random.randint(75, 100),
                               InstapyFollowed=(True, "nonfollowers"),
                               style="FIFO",
                               unfollow_after=24 * 60 * 60, sleep_delay=600)

        session.unfollow_users(amount=random.randint(75, 100),
                               InstapyFollowed=(True, "all"), style="FIFO",
                               unfollow_after=168 * 60 * 60, sleep_delay=600)

        session.join_pods()


def load_users_to_follow(db_path, users_num):
    conn = sqlite3.connect(db_path)

    with conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "SELECT username FROM followRestriction WHERE profile_id={pr_id} AND username IN ({usr});"\
            .format(pr_id=id, usr=','.join(map(str, ["\'{}\'".format(user) for user in users])))
        cur.execute(sql)
        users_interacted = [dict(row)['username'] for row in cur.fetchall()]
        return list(set(users) - set(users_interacted))


def find_users_not_interacted(users):
    db, id = get_database()
    conn = sqlite3.connect(db)

    with conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "SELECT username FROM followRestriction WHERE profile_id={pr_id} AND username IN ({usr});"\
            .format(pr_id=id, usr=','.join(map(str, ["\'{}\'".format(user) for user in users])))
        cur.execute(sql)
        users_interacted = [dict(row)['username'] for row in cur.fetchall()]
        return list(set(users) - set(users_interacted))


if __name__== "__main__":
    main()