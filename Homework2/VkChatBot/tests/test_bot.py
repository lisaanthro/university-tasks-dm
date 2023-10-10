import pytest

from bot import UserStatus, group_id, user_notify_time

user_id = 259909233

user = UserStatus(user_id)


def test_user_id():
    assert user.user_id == user_id


def test_greeting():
    user.greetings('привет')
    assert user.state == 1


def test_city_choice_from_console():
    user.city_input('aaaa')
    user._send_forecast()
    assert user.state == 1
def test_city_choice_incorrect():
    user.city_choice(message='Some random message')
    assert user.state == 1

def test_city_choice_from_profile_test():
    user.city_choice(message='Взять город из профиля')
    assert user.state == 3
#



def test_city_choice_from_console_correct():
    user.state = 2
    user.city_input('Москва')
    assert user.city == 'Москва'


def test_range_negative():
    user.range_choice('-100')
    assert user.range == 1


def test_range_max():
    user.range_choice('100')
    assert user.range == 1


def test_range_string():
    user.range_choice('abc100')
    assert user.range == 1


def test_range_correct():
    user.range_choice('3')
    assert user.range == 3


def test_notif_choice_incorrect():
    user.notification_choice('aaaaa')
    assert user.state == 4


def test_notif_choice_no():
    user.notification_choice('Да')
    assert user.state == 5


def test_notif_string():
    user.notification_add('afj;a;')
    assert user.user_id not in user_notify_time


def test_notif_invalid_numbers():
    user.notification_add('-11:65')
    assert user.user_id not in user_notify_time


def test_notif_correct():
    user.notification_add('11:55')
    assert user.notif_time == '11:55'
    assert user.user_id in user_notify_time
