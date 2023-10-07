import pytest

from bot import UserStatus, group_id

user_id = 259909233

user = UserStatus(user_id)


def city_choice_from_profile_test():
    pass
    with pytest.raises(KeyError):
        user.city_choice(message='Взять город из профиля')


def city_choice_from_colsole():
    user.city_input('aaaa')
    assert user.city == ''


def range_negative():
    user.range_choice('-100')
    print(user.state, user.range)
    # assert user.state == 3


user.greetings("a")
user.city_choice("Взять город из профиля")
range_negative()
# while True:
#     message = input()
#     user.next(message)
