import random
import sys
import sqlite3

from instapy import InstaPy, Settings
from instapy import smart_run
from instapy import set_workspace

comments = [u'Приглашаю подписаться на мой блог о детском питании и материнстве. Вопросы и комментарии приветствуются!:baby:',
            u'Подписывайтесь на мой блог о грудном, искусственном вскармливании и о прикорме. Отвечу на все Ваши вопросы!:baby:',
            u'Приглашаю подписаться на мой блог о детском питании и материнстве. Много полезной информации, ответы на Ваши вопросы!:baby:',
            u'Отвечу на Ваши вопросы о грудном, искусственном вскармливании и о прикорме. Подписывайтесь, много полезной и актуальной информации!:baby:',
            u'Хотите узнать все о грудном и искусственном вскармливании и о прикорме, тогда подписывайтесь на мой блог. Отвечу на интересующие Вас вопросы!:baby:',
            u'В моем блоге Вы найдете самую полезную и актуальную информацию о грудном, искусственном вскармливании и о прикорме. Подписывайтесь обязательно!:baby:',
            u'В моем блоге Вы найдете ответы на все интересующие вопросы о грудном, искусственном вскармливании и о прикорме. Обязательно подписывайтесь!:baby:',
            u'Хотите знать все о детском питании (гв, ив, прикорм), тогда подписывайтесь на мой блог. Отвечу на все интересующие Вас вопросы!:baby:',
            u'Самая актуальная информация о детском питании (гв, ив, прикорм) у маня в блоге. Подписывайтесь обязательно!:baby:',
            u'Много полезной информации о грудном, искусственном вскармливании и о прикорме у меня в блоге. Подписывайтесь, отвечу на все интересующие Вас вопросы!:baby:']


def main():
    # login credentials
    insta_username = sys.argv[1]
    insta_password = sys.argv[2]
    target_profile = sys.argv[3]
    users_num = sys.argv[4]
    workspace_path = sys.argv[5]

    set_workspace(path=workspace_path)

    target_users = load_users_to_follow(target_profile, users_num)

    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      disable_image_load=True,
                      multi_logs=True)

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

        session.set_skip_users(skip_private=False)

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "follows", "unfollows", "server_calls_h"],
                                     sleepyhead=True,
                                     stochastic_flow=True,
                                     notify_me=True,
                                     peak_likes=(50, 110),
                                     peak_follows=(50, 110),
                                     peak_unfollows=(50, 120),
                                     peak_server_calls=(1000, 3000))

        session.set_user_interact(amount=3, randomize=True, percentage=90, media='Photo')
        session.set_do_like(enabled=True, percentage=80)
        session.set_do_comment(enabled=True, percentage=25)
        session.set_comments(comments)
        session.set_do_follow(enabled=True, percentage=40, times=1)

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


def load_users_to_follow(target_profile, users_num):
    conn = sqlite3.connect(Settings.database_location)

    with conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "SELECT name FROM liker l INNER JOIN post p ON l.post_link = p.link WHERE p.profile_name='{}' " \
              "AND name NOT IN (SELECT username FROM followRestriction) " \
              "ORDER BY crawling_order LIMIT {};"\
            .format(target_profile, users_num)
        cur.execute(sql)
        return [dict(row)['name'] for row in cur.fetchall()]


if __name__== "__main__":
    main()