import vk_api
import threading, schedule, time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from forecast import ForecastApi
from keyboards import start_keyboard, notif_keyboard
from keys import keyboard_keys, api_key
from message import message1, message2

group_id = 222705703

vk_session = vk_api.VkApi(token=api_key)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

user_actions = dict()
user_notify_time = dict()

forecast_api = ForecastApi()


def notif_thread():
    while True:
        schedule.run_pending()
        time.sleep(60)


threading.Thread(target=notif_thread).start()


class UserStatus:
    'Класс пользователя. state: 0 - получает информацию о функциях бота, 1 - выбор города, 2 - выбор диапозона (сегодня, n дней) или выбор уведомлений'

    def __init__(self, user_id):
        self.state = 0
        self.user_id = user_id
        self.range = 1
        self.last_message = ""
        self.notif_time = ""
        self.city = ""
        self.actions = [self.greetings, self.city_choice, self.city_input, self.range_choice, self.notification_choice,
                        self.notification_add]

    def greetings(self, message):
        self.last_message = message
        vk.messages.send(keyboard=start_keyboard.get_keyboard(),
                         key=keyboard_keys['key'],
                         server=keyboard_keys['server'],
                         ts=keyboard_keys['ts'],
                         user_id=self.user_id,
                         random_id=get_random_id(),
                         message=message1)
        self.state += 1

    def city_choice(self, message):
        # city from profile
        if message == 'Взять город из профиля':
            user_city_json = vk.users.get(user_id=self.user_id, fields='city')[0].get('city')
            try:
                user_city = user_city_json.get('title')
                self.city = user_city
                vk.messages.send(user_id=self.user_id,
                                 random_id=get_random_id(),
                                 message=f'г. {self.city}. ' + message2)
                self.state += 1
            except Exception:
                vk.messages.send(user_id=self.user_id,
                                 random_id=get_random_id(),
                                 message='Кажется, у тебя в профиле не указан город.')
                self.state = 0
                return
        elif message == 'Указать город':
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Введи название города с большой буквы.')
        else:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Что-то странное, введи данные еще раз.')
            return
        self.state += 1

    def city_input(self, message):
        try:
            self.city = message
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'г. {self.city}. ' + message2)
            self.state += 1
        except ValueError:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Ошибка, город не найден.')
            self.state = 1

    def range_choice(self, message):
        if message.isdigit() and 1 <= int(message) <= 10:
            self.range = int(message)
            self.state += 1
            vk.messages.send(keyboard=notif_keyboard.get_keyboard(),
                             key=keyboard_keys['key'],
                             server=keyboard_keys['server'],
                             ts=keyboard_keys['ts'],
                             user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Хочешь получать уведомления о погоде?')
        else:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Повтори введение дипапзона: целое число от 1 до 10 без посторинних данных.')

    def notification_choice(self, message):
        if message == 'Да':
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Введите время в формате hh:mm')
            self.state += 1
        elif message == 'Нет':
            self._send_forecast()
        else:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Выберите "Да" или "Нет".')
            self.state = 3
            self.next(str(self.range))

    def notification_add(self, message):
        message_list = message.strip(' ').split(':')
        if len(message_list) == 2 and len(message_list[0]) == len(message_list[1]) == 2 and self._check_time(
                message_list):
            user_notify_time[self.user_id] = message
            schedule.every().day.at(message).do(self._send_forecast)
            self.notif_time = message
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Уведомления настроены!')  # add city to notif
            self.state += 1
            self._send_forecast()
        else:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Неверный формат ввода времени.')
            self.state = 3
            self.next(str(self.range))

    @staticmethod
    def _check_time(message: list):
        num1 = int(message[0])
        num2 = int(message[1])
        if 0 <= num1 <= 23 and 0 <= num2 <= 59:
            return True
        return False

    def _send_forecast(self):
        try:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=f'Отправляю прогноз погоды в {self.city}...')
            forecast = forecast_api.get_forecast(self.city, self.range)
            if 'error' in forecast:
                raise ValueError
            # print(forecast)
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message=forecast)
            self.state = 0
        except ValueError:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Кажется, что-то не так с названием города. Повтори попытку.')
            self.state = 0
        except:
            vk.messages.send(user_id=self.user_id,
                             random_id=get_random_id(),
                             message='Кажется, что-то не так с api. Прошу сообщить разработчику.')
            self.state = 0
        self.next("")

    def next(self, message):
        if message == 'Стоп':
            self.state = 0
        next_func = self.actions[self.state]
        next_func(message)

    def __str__(self):
        return f'{self.user_id=}, {self.state=}'


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            if user_id not in user_actions:
                user_actions[user_id] = UserStatus(user_id)
            user = user_actions[user_id]
            user.next(message=event.text)


if __name__ == '__main__':
    main()
