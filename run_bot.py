import random
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace

set_workspace(path="/home/pi/IG/Workspace")

# login credentials
insta_username = ''
insta_password = ''

# restriction data
dont_likes = ['#exactmatch', '[startswith', ']endswith', 'broadmatch']
ignore_users = ['user1', 'user2', 'user3']

friends = ['friend1', 'friend2', 'friend3']

ignore_list = []

targets = ['vopros_gv']

target_business_categories = ['category1', 'category2', 'category3']

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  disable_image_load=True,
                  multi_logs=True)

with smart_run(session):
    # session.set_dont_include(friends)
    # session.set_dont_like(dont_likes)
    # session.set_ignore_if_contains(ignore_list)
    # session.set_ignore_users(ignore_users)
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

    session.set_skip_users(skip_private=False,
                           skip_no_profile_pic=True,
                           skip_business=True,
                           dont_skip_business_categories=[target_business_categories])

    session.set_quota_supervisor(enabled=True,
                                 sleep_after=["likes", "follows", "unfollows", "server_calls_h"],
                                 sleepyhead=True,
                                 stochastic_flow=True,
                                 notify_me=True,
                                 peak_likes=(32, 110),
                                 peak_follows=(31, 110),
                                 peak_unfollows=(35, 120),
                                 peak_server_calls=(1000, 3000))

    session.set_user_interact(amount=3, randomize=True, percentage=90, media='Photo')
    session.set_do_like(enabled=True, percentage=80)
    session.set_do_follow(enabled=True, percentage=20, times=1)

    # activities
    session.follow_user_followers(targets,
                                  amount=random.randint(50, 80),
                                  randomize=True, sleep_delay=600,
                                  interact=True)

    session.unfollow_users(amount=random.randint(75, 100),
                           InstapyFollowed=(True, "nonfollowers"),
                           style="FIFO",
                           unfollow_after=24 * 60 * 60, sleep_delay=600)

    session.unfollow_users(amount=random.randint(75, 100),
                           InstapyFollowed=(True, "all"), style="FIFO",
                           unfollow_after=168 * 60 * 60, sleep_delay=600)

    session.join_pods()