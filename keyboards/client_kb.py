from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


olx_btn = KeyboardButton('Olx')
autoria_btn = KeyboardButton('Auto.ria')

choose_parsers = ReplyKeyboardMarkup(resize_keyboard=True)
choose_parsers.add(olx_btn).insert(autoria_btn)


create_link_btn = KeyboardButton('Создать ссылку Olx')
my_links = KeyboardButton('Мои ссылки c Olx')
remove_link = KeyboardButton('Удалить ссылки Olx')
returned_btn = KeyboardButton('Вернуться к агрегаторам')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(create_link_btn).add(my_links).insert(remove_link).row(returned_btn)

create_link_btn_auto = KeyboardButton('Создать ссылку Auto.ria')
my_links_auto = KeyboardButton('Мои ссылки с Auto.ria')
remove_link_auto = KeyboardButton('Удалить ссылки Auto.ria')
returned_btn_auto = KeyboardButton('Вернуться к агрегаторам')

kb_client_auto = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_auto.add(create_link_btn_auto).add(my_links_auto).insert(remove_link_auto).row(returned_btn_auto)
