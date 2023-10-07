import pytest

from bot import UserStatus, group_id, user_notify_time

user_id = 259909233

user = UserStatus(user_id)


# def test_city_choice_from_profile_test():
#     user.city_choice(message='Взять город из профиля')
#
#
# def test_city_choice_from_console():
#     user.city_input('aaaa')
#     user._send_forecast()
#
#
# def test_city_choice_from_console_correct():
#     user.city_input('Москва')
#     assert user.city == 'Москва'
#
#
# def test_range_negative():
#     user.range_choice('-100')
#     print(user.state, user.range)
#     assert user.range == 1
#
#
# def test_range_max():
#     user.range_choice('100')
#     assert user.range == 1
#
#
# def test_range_string():
#     user.range_choice('abc100')
#     assert user.range == 1
#
#
# def test_range_correct():
#     user.range_choice('3')


def test_notif_string():
    user.notification_add('afj;a;')
    assert user.user_id not in user_notify_time


def test_notif_invalid_numbers():
    user.notification_add('-11:65')
    assert user.user_id not in user_notify_time


def test_notif_correct():
    user.notification_add('11:55')
    # assert user.notif_time == '11:55'
    assert user.user_id in user_notify_time
