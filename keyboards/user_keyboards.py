from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_start_user() -> ReplyKeyboardMarkup:
    logging.info("keyboards_start_user")
    button_1 = KeyboardButton(text='🏠 Главное меню')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], ],
        resize_keyboard=True
    )
    return keyboard


def keyboard_bay_sell() -> InlineKeyboardMarkup:
    logging.info("keyboard_bay_sell")
    button_1 = InlineKeyboardButton(text='Купить',  callback_data=f'estate_bay')
    button_2 = InlineKeyboardButton(text='Продать', callback_data=f'estate_sell')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard


def keyboard_type_estate_real() -> InlineKeyboardMarkup:
    logging.info("keyboard_type_estate_real")
    button_1 = InlineKeyboardButton(text='Земельный участок',  callback_data=f'type_estate_land')
    button_2 = InlineKeyboardButton(text='Дом', callback_data=f'type_estate_house')
    button_3 = InlineKeyboardButton(text='Квартиру', callback_data=f'type_estate_flat')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]], )
    return keyboard


def keyboard_type_land() -> ReplyKeyboardMarkup:
    logging.info("keyboard_type_land")
    button_1 = KeyboardButton(text='Север (Выборгский, Приозерский, Всеволожский р-н)')
    button_2 = KeyboardButton(text='ЮГ (Гатчинский, Ломоносовский, Тосненский, Красносельский)')
    button_3 = KeyboardButton(text='Юго-восток (Кировский, Всеволожский)')
    button_4 = KeyboardButton(text='Только в границе СПБ')
    button_5 = KeyboardButton(text='Другой вариант')
    button_6 = KeyboardButton(text='🏠 Главное меню')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5], [button_6]],
        resize_keyboard=True
    )
    return keyboard


def keyboard_type_estate_house() -> InlineKeyboardMarkup:
    logging.info("keyboard_type_estate_house")
    button_1 = InlineKeyboardButton(text='Да',  callback_data=f'type_house_Да')
    button_2 = InlineKeyboardButton(text='Нет', callback_data=f'type_house_Нет')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard


def keyboard_phone() -> ReplyKeyboardMarkup:
    logging.info(f'keyboard_phone')
    button_1 = KeyboardButton(text='Поделиться ☎️', request_contact=True)
    button_2 = KeyboardButton(text='🏠 Главное меню')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2]], resize_keyboard=True
    )
    return keyboard


def keyboard_type_land_area() -> InlineKeyboardMarkup:
    logging.info("keyboard_type_land_area")
    button_1 = InlineKeyboardButton(text='6 - 8 соток',  callback_data=f'land_area_6-8')
    button_2 = InlineKeyboardButton(text='8 - 12 соток',  callback_data=f'land_area_8-12')
    button_3 = InlineKeyboardButton(text='12 - 15 соток',  callback_data=f'land_area_12-15')
    button_4 = InlineKeyboardButton(text='от 15 соток', callback_data=f'land_area_от 15')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]])
    return keyboard


def keyboard_type_wall() -> InlineKeyboardMarkup:
    logging.info("keyboard_type_wall")
    button_1 = InlineKeyboardButton(text='Каменный',  callback_data=f'type_wall_Каменный')
    button_2 = InlineKeyboardButton(text='Деревянный',  callback_data=f'type_wall_Деревянный')
    button_3 = InlineKeyboardButton(text='Каркасный',  callback_data=f'type_wall_Каркасный')
    button_4 = InlineKeyboardButton(text='Другое', callback_data=f'type_wall_other')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]])
    return keyboard


def keyboard_budget() -> InlineKeyboardMarkup:
    logging.info("keyboard_budget")
    button_1 = InlineKeyboardButton(text='от 7 500 000 до 10 000 000',  callback_data=f'budget_от 7 500 000 до 10 000 000')
    button_2 = InlineKeyboardButton(text='от 10 000 000 до 15 000 000',  callback_data=f'budget_от 10 000 000 до 15 000 000')
    button_3 = InlineKeyboardButton(text='от 15 000 000',  callback_data=f'budget_от 15 000 000')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]])
    return keyboard


def keyboard_payment_option() -> InlineKeyboardMarkup:
    logging.info("keyboard_type_type_wall")
    button_1 = InlineKeyboardButton(text='Ипотека',  callback_data=f'payment_option_Ипотека')
    button_2 = InlineKeyboardButton(text='Наличные',  callback_data=f'payment_option_Наличные')
    button_3 = InlineKeyboardButton(text='Встречная продажа',  callback_data=f'payment_option_Встречная продажа')
    button_4 = InlineKeyboardButton(text='Сертификат', callback_data=f'payment_option_Сертификат')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]])
    return keyboard


def keyboard_deadline() -> InlineKeyboardMarkup:
    logging.info("keyboard_deadline")
    button_1 = InlineKeyboardButton(text='Сейчас',  callback_data=f'deadline_сейчас')
    button_2 = InlineKeyboardButton(text='1-3 месяца',  callback_data=f'deadline_1-3 месяца')
    button_3 = InlineKeyboardButton(text='от 3 месяцев',  callback_data=f'deadline_от 3 месяцев')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]])
    return keyboard


def keyboard_deadline_house() -> InlineKeyboardMarkup:
    logging.info("keyboard_deadline")
    button_1 = InlineKeyboardButton(text='Сейчас',  callback_data=f'deadline_сейчас')
    button_2 = InlineKeyboardButton(text='1-3 месяца',  callback_data=f'deadline_1-3 месяца')
    button_3 = InlineKeyboardButton(text='от 3 до 6 месяцев',  callback_data=f'deadline_от 3 до 6 месяцев')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]])
    return keyboard