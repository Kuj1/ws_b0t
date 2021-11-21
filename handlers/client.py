from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hide_link
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.olx_db import sql_add_link, sql_read_olx_link, sql_remove_olx_link
from db.ria_db import sql_add_link_to_ria, sql_read_ria_link, sql_remove_ria_link
from create_bot import dp
from keyboards import kb_client
from keyboards import kb_client_auto
from keyboards import choose_parsers
from parsers import sql_output_olx_link, olx, sql_output_ria_link, auto_ria


class FsmCreateLinkAuto(StatesGroup):
    create_auto = State()


class FsmCreateLink(StatesGroup):
    create = State()


class FsmRemoveLink(StatesGroup):
    remove = State()


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


# После этой функции начинается парсинг и показ результата
async def create_link_olx(message: types.Message, state: FSMContext):
    async with state.proxy() as url:
        url['url_olx'] = message.text

    await sql_add_link(state)
    await message.answer('Ссылка создана')

    url_for_olx = sql_output_olx_link()
    result_olx = olx(url=url_for_olx)

    # Этот срез очень важен, его лучше не убирать иначе TypeError
    for check_items in result_olx[0: -1]:
        parse_items = f'{hide_link(check_items["item_photo"])} ' \
                      f'\n{hbold("Местоположение", ": ")}{check_items["item_city"]}' \
                      f'\n{hbold("Наименование", ": ")}{check_items["item_title"]}' \
                      f'\n{hbold("Цена", ": ")}{check_items["item_price"]}' \
                      f'\n{hide_link(check_items["item_photo"])}'

        inline_kb_olx = InlineKeyboardMarkup()
        inline_kb_olx.add(InlineKeyboardButton('Перейти по ссылке', url=f'{check_items["item_url"]}'))
        await message.answer(parse_items, parse_mode="HTML", reply_markup=inline_kb_olx)
    await state.finish()


async def show_links_olx(message: types.Message):
    read = await sql_read_olx_link()
    for link in read:
        await message.answer(str(link).strip("('").strip("')").strip(",").strip("'"))


async def removing_link_olx(message: types.Message):
    await sql_remove_olx_link()
    await message.answer('Ссылки удалены')


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

    await sql_add_link_to_ria(state)
    await message.answer('Ссылка создана')

    url_for_ria = sql_output_ria_link()
    result_ria = auto_ria(url=url_for_ria)

    for check_items in result_ria[0: -1]:
        parse_items = f'{hide_link(check_items["item_photo"])} ' \
                      f'\n{hbold("Местоположение", ": ")}{check_items["item_city"]}' \
                      f'\n{hbold("Наименование", ": ")}{check_items["item_title"]}' \
                      f'\n{hbold("Цена", ": ")}{check_items["item_price"]}' \
                      f'\n{hbold("Ссылка", ": ")}{check_items["item_url"]}' \
                      f'\n{hide_link(check_items["item_photo"])}'

        inline_kb_ria = InlineKeyboardMarkup()
        inline_kb_ria.add(InlineKeyboardButton('Перейти по ссылке', url=f'{check_items["item_url"]}'))

        await message.answer(parse_items, parse_mode="HTML", reply_markup=inline_kb_ria)
    await state.finish()


async def show_links_autoria(message: types.Message, state: FSMContext):
    read = await sql_read_ria_link()
    for link in read:
        await message.answer(str(link).strip("('").strip("')").strip(",").strip("'"))


async def removing_link_ria(message: types.Message):
    await sql_remove_ria_link()
    await message.answer('Ссылки удалены')


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], content_types=['text'], state=None)
    dp.register_message_handler(cancel_btn, Text(equals='Вернуться к агрегаторам'), state='*')
    dp.register_message_handler(start_olx, Text('Olx'), content_types=['text'])
    dp.register_message_handler(start_create_link_olx, Text('Создать ссылку Olx'), state=None)
    dp.register_message_handler(link_invalid_olx, lambda message: 'https://www.olx.ua/' not in message.text,
                                state=FsmCreateLink.create)
    dp.register_message_handler(create_link_olx, content_types=['text'], state=FsmCreateLink.create)
    dp.register_message_handler(show_links_olx, Text('Мои ссылки'))
    dp.callback_query_handler(lambda x: x.data and x.data.startwith('del '))
    dp.register_message_handler(removing_link_olx, Text('Удалить ссылки Olx'))
    dp.register_message_handler(start_autoria, Text('Auto.ria'), content_types=['text'])
    dp.register_message_handler(start_create_link_autoria, Text('Создать ссылку Auto.ria'), state=None)
    dp.register_message_handler(link_invalid_autoria, lambda message: 'https://auto.ria.com/' not in message.text,
                                state=FsmCreateLinkAuto.create_auto)
    dp.register_message_handler(create_link_autoria, content_types=['text'], state=FsmCreateLinkAuto.create_auto)
    dp.register_message_handler(show_links_autoria, Text('Мои ссылки'), state=FsmMyLinks.show_links)
    dp.register_message_handler(removing_link_ria, Text('Удалить ссылки Auto.ria'))
