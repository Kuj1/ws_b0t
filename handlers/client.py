from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from db.olx_db import sql_add_link
from create_bot import dp
from keyboards import kb_client
from keyboards import kb_client_auto
from keyboards import choose_parsers


class FsmCreateLinkAuto(StatesGroup):
    create_auto = State()


class FsmCreateLink(StatesGroup):
    create = State()


class FsmMyLinks(StatesGroup):
    show_links = State()


async def command_start(message: types.Message):
    await message.answer("""
1.Найдите интересующий вас товар на сайте OLX.UA 💎📷💍🚗, по выгодной вам цене💵 
2.Нажмите в панели ,создать ссылку 📎📎📎 
Вы  можете использовать мобильную версию браузера 
пример ссылки : [ https://m.olx.ua/nedvizhimost/ ]
🚨Внимание🚨
Для наиболее качественного результата ИСПОЛЬЗУЙТЕ 
     📍полную версию📍сайта OLX  в браузере 🚨Chrome🚨
Пример ссылки : [ https://www.olx.ua/uk/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/ko/?search%5Bfilter_float_price%3Ato%5D=3000000 ]
🚨Смотреть ВИДЕО ИНСТРУКЦИЮ
3.Скопируйте ссылку интересующего вас фильтра в бота 💾 💾💾
4. Как только объявление по вашим критериям появится на сайте OLX.ua - вы получите уведомление первым!👍🏻 💵💶💷

🔑🔑🔑Что бы добавить дополнительную ссылку напишите администратору ✍🏻✍🏻✍🏻

🚨🚨🚨Внимание смотреть ВИДЕО ИНСТРУКЦИЮ для Android🚨🚨🚨
https://youtu.be/uxImf35UNUE
🚨🚨🚨Внимание смотреть ВИДЕО ИНСТРУКЦИЮ для  IPhone🚨🚨🚨
https://youtu.be/8tOxQjOZ0Kg""", reply_markup=choose_parsers,)
    await message.answer('Выберите агрегатор')


async def cancel_btn(message: types.Message, state: FSMContext):
    # Думаю на данном этапе здесь эта логика не нужна, но на всякий
    # current_state = await state.get_state()
    # if current_state is None:
    #     return
    await state.finish()
    await message.reply('Вернулись к выбору агрегатора', reply_markup=choose_parsers)


async def start_olx(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=kb_client)


async def start_create_link_olx(message: types.Message):
    await message.reply('Введите ссылку:')
    await FsmCreateLink.create.set()


# если ссылка не валидна
async def link_invalid_olx(message: types.Message):
    await message.answer("""🚨Внимание смотреть видео инструкцию для IPhone 🚨https://youtu.be/8tOxQjOZ0Kg
🚨Внимание смотреть ВИДЕО ИНСТРУКЦИЮ для Android 🚨
https://youtu.be/uxImf35UNUE
1.Откоройте сайт OLX.ua📌 и найдите интересующий вас товар или услугу по интересующим вас фильтрам 🚗📱💎
Вы  можете использовать мобильную версию браузера 
пример ссылки : [ https://m.olx.ua/nedvizhimost/ ]
🚨Внимание🚨
Для наиболее качественного результата ИСПОЛЬЗУЙТЕ 
     📍полную версию📍сайта OLX  в браузере 🚨Chrome🚨
Пример ссылки : [ https://www.olx.ua/uk/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/ko/?search%5Bfilter_float_price%3Ato%5D=3000000 ]
2.Скопируйте ссылку с сайта OLX.ua 💾💾💾
3.Вставьте ссылку сюда ⬇️⬇️⬇️
🔑🔑🔑Что бы добавить дополнительную ссылку напишите администратору @Brookland✍🏻✍🏻✍🏻""")


async def create_link_olx(message: types.Message, state: FSMContext):
    async with state.proxy() as url:
        url['url_olx'] = message.text

    await sql_add_link(state)
    await message.answer('Ссылка создана')
    # после этого начинается парсинг раз в минуту
    await state.finish()


async def show_links_olx(message: types.Message):
    await message.reply('Вот они')
    # подтягивается ссылка из БД. Пока подтягивает из memory storage


# Здесь надо реализовать функцию удаления ссылки


async def start_autoria(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=kb_client_auto)


async def start_create_link_autoria(message: types.Message):
    await message.reply('Введите ссылку:')
    await FsmCreateLinkAuto.create_auto.set()


# если ссылка не валидна
async def link_invalid_autoria(message: types.Message):
    await message.answer("""🚨Внимание смотреть видео инструкцию для IPhone 🚨https://youtu.be/8tOxQjOZ0Kg
🚨Внимание смотреть ВИДЕО ИНСТРУКЦИЮ для Android 🚨
https://youtu.be/uxImf35UNUE
1.Откоройте сайт OLX.ua📌 и найдите интересующий вас товар или услугу по интересующим вас фильтрам 🚗📱💎
Вы  можете использовать мобильную версию браузера 
пример ссылки : [ https://m.olx.ua/nedvizhimost/ ]
🚨Внимание🚨
Для наиболее качественного результата ИСПОЛЬЗУЙТЕ 
     📍полную версию📍сайта OLX  в браузере 🚨Chrome🚨
Пример ссылки : [ https://www.olx.ua/uk/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/ko/?search%5Bfilter_float_price%3Ato%5D=3000000 ]
2.Скопируйте ссылку с сайта OLX.ua 💾💾💾
3.Вставьте ссылку сюда ⬇️⬇️⬇️
🔑🔑🔑Что бы добавить дополнительную ссылку напишите администратору @Brookland✍🏻✍🏻✍🏻""")


async def create_link_autoria(message: types.Message, state: FSMContext):
    async with state.proxy() as url:
        url['url_autoria'] = message.text
    await message.answer('Ссылка создана')
    # после этого начинается парсинг раз в минуту
    await state.finish()


async def show_links_autoria(message: types.Message, state: FSMContext):
    await message.reply('Вот они')
    # подтягивается ссылка из БД. Пока подтягивает из memory storage


# Здесь надо реализовать функцию удаления ссылки


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], content_types=['text'], state=None)
    dp.register_message_handler(cancel_btn, Text(equals='Вернуться к агрегаторам'), state='*')
    dp.register_message_handler(start_olx, Text('Olx'), content_types=['text'])
    dp.register_message_handler(start_create_link_olx, Text('Создать ссылку Olx'), state=None)
    dp.register_message_handler(link_invalid_olx, lambda message: 'https://www.olx.ua/' not in message.text,
                                state=FsmCreateLink.create)
    dp.register_message_handler(create_link_olx, content_types=['text'], state=FsmCreateLink.create)
    dp.register_message_handler(show_links_olx, Text('Мои ссылки'))
    dp.register_message_handler(start_autoria, Text('Auto.ria'), content_types=['text'])
    dp.register_message_handler(start_create_link_autoria, Text('Создать ссылку Auto.ria'), state=None)
    dp.register_message_handler(link_invalid_autoria, lambda message: 'https://auto.ria.com/' not in message.text,
                                state=FsmCreateLinkAuto.create_auto)
    dp.register_message_handler(create_link_autoria, content_types=['text'], state=FsmCreateLinkAuto.create_auto)
    dp.register_message_handler(show_links_autoria, Text('Мои ссылки'), state=FsmMyLinks.show_links)
