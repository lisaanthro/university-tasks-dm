from vk_api.keyboard import VkKeyboard, VkKeyboardColor

start_keyboard = VkKeyboard(one_time=True)
start_keyboard.add_button('Взять город из профиля', color=VkKeyboardColor.NEGATIVE)
start_keyboard.add_button('Указать город', color=VkKeyboardColor.NEGATIVE)

notif_keyboard = VkKeyboard(one_time=True)
notif_keyboard.add_button('Да', color=VkKeyboardColor.NEGATIVE)
notif_keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
