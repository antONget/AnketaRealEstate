from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import user_keyboards as kb
from config_data.config import Config, load_config
from database import requests as rq
from utils.error_handling import error_handler
from filter.filter import validate_russian_phone_number
from utils.send_admins import send_message_admins
import logging
router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    input_other = State()
    type_wall = State()
    phone = State()


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Пользовательский режим запускается если, пользователь ввел команду /start
    1. Добавляем пользователя в БД если его еще нет в ней
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.set_state(state=None)
    await state.clear()
    if message.from_user.username:
        username = message.from_user.username
    else:
        username = 'username'
    await rq.add_user(tg_id=message.chat.id,
                      data={"tg_id": message.chat.id, "username": username})
    await message.answer(text=f'Добро пожаловать!',
                         reply_markup=kb.keyboards_start_user())
    await message.answer(text=f'Что вы хотите?',
                         reply_markup=kb.keyboard_bay_sell())


@router.message(F.text == '🏠 Главное меню')
async def main_menu(message: Message, state: FSMContext, bot: Bot):
    """
    Переход к главному окну
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.set_state(state=None)
    await state.clear()
    await process_start_command_user(message=message, state=state, bot=bot)


@router.callback_query(F.data.startswith("estate_"))
@error_handler
async def type_real_estate(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Выбор типа недвижимости [Земельный участок, Дом, Квартира]
    :param callback: [estate_bay, estate_sell]
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'type_real_estate {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(payment=answer)
    if answer == 'sell':
        await callback.message.edit_text(text=f'Какой тип недвижимости Вы хотите продать?',
                                         reply_markup=kb.keyboard_type_estate_real())
    else:
        await callback.message.edit_text(text=f'Какой тип недвижимости Вы ищете?',
                                         reply_markup=kb.keyboard_type_estate_real())
    await callback.answer()


@router.callback_query(F.data.startswith("type_estate_"))
@error_handler
async def type_real_estate(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Разветвление в зависимости от типа недвижимости
    :param callback: [type_estate_land, type_estate_house, type_estate_flat]
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'type_real_estate {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(type=answer)
    data = await state.get_data()
    if data['payment'] == 'sell':
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        if answer == 'land':
            await state.update_data(type_e="Земельный участок")
        elif answer == 'house':
            await state.update_data(type_e="Дом")
        elif answer == 'flat':
            await state.update_data(type_e="Квартира")
        await callback.message.answer(text=f'Оставьте номер телефона наш специалист Вам перезвонит',
                                      reply_markup=kb.keyboard_phone())
        await state.set_state(await state.set_state(User.phone))
        await callback.answer()
        return
    if answer == 'land':
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        await callback.message.answer(text=f'Какое направление интересует?',
                                      reply_markup=kb.keyboard_type_land())
        await state.update_data(type_e="Земельный участок")
    elif answer == 'house':
        await callback.message.edit_text(text=f'Рассматриваете строительство?',
                                         reply_markup=kb.keyboard_type_estate_house())
        await state.update_data(type_e="Дом")
    elif answer == 'flat':
        await callback.message.answer(text=f'Оставьте номер телефона наш специалист Вам перезвонит',
                                      reply_markup=kb.keyboard_phone())
        await state.update_data(type_e="Квартира")
        await state.set_state(User.phone)
    await callback.answer()


@router.callback_query(F.data.startswith('type_house'))
@error_handler
async def process_house(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем сведения об участке для дома и запрашиваем направление
    :param callback: type_house_yes
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'type_real_estate {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(land=answer)
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await callback.message.answer(text=f'Какое направление интересует?',
                                  reply_markup=kb.keyboard_type_land())
    await callback.answer()


@router.message(F.text == 'Другой вариант')
@error_handler
async def process_input_other(message: Message, state: FSMContext, bot: Bot):
    """
    Ожидаем ввод пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await message.answer(text=f'Напишите ваш вариант?')
    await state.set_state(User.input_other)


@router.message(lambda message: message.text in ['Север (Выборгский, Приозерский, Всеволожский р-н)',
                                                 'ЮГ (Гатчинский, Ломоносовский, Тосненский, Красносельский)',
                                                 'Юго-восток (Кировский, Всеволожский)',
                                                 'Только в границе СПБ'])
@router.message(StateFilter(User.input_other))
@error_handler
async def get_input_other(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем ввод пользователя ввод пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_input_other: {message.chat.id}')
    await state.set_state(state=None)
    # await message.answer(text='Отлично ',
    #                      reply_markup=ReplyKeyboardRemove())
    await message.answer(text='Отлично ',
                         reply_markup=kb.keyboards_start_user())
    # await bot.delete_message(chat_id=message.chat.id,
    #                          message_id=message.message_id + 1)
    # await bot.delete_message(chat_id=message.chat.id,
    #                          message_id=message.message_id + 2)
    data = await state.get_data()
    if data['type'] == 'land':
        await state.update_data(district=message.text)
        await message.answer(text=f'Какой площади участок вы рассматриваете?',
                             reply_markup=kb.keyboard_type_land_area())
    elif data['type'] == 'house':
        await state.update_data(district=message.text)
        await message.answer(text=f'Тип материала дома?',
                             reply_markup=kb.keyboard_type_wall())


@router.callback_query(F.data.startswith('land_area'))
@error_handler
async def get_land_area(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем площадь участка
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_land_area {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(land_area=answer)
    await callback.message.edit_text(text='Какой вариант оплаты будете использовать?',
                                     reply_markup=kb.keyboard_payment_option())
    await callback.answer()


@router.callback_query(F.data.startswith('payment_option'))
@error_handler
async def get_payment_option(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем способ оплаты
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_payment_option {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    data = await state.get_data()
    if data['type'] == 'land':
        await state.update_data(payment_option=answer)
        await callback.message.edit_text(text='В какие сроки готовы приобретать участок?',
                                         reply_markup=kb.keyboard_deadline())
    elif data['type'] == 'house':
        await state.update_data(payment_option=answer)
        await callback.message.edit_text(text='В какие сроки готовы выйти на сделку?',
                                         reply_markup=kb.keyboard_deadline_house())
    await callback.answer()


@router.callback_query(F.data.startswith('deadline'))
@error_handler
async def get_deadline(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем срок выхода на сделку
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_deadline {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(deadline=answer)
    await state.set_state(User.phone)
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await callback.message.answer(text=f'Оставьте номер телефона наш специалист Вам перезвонит',
                                  reply_markup=kb.keyboard_phone())



    # await callback.message.answer(text='Благодарим вас за ответы, менеджер свяжется с вами в ближайшее время')
    # await callback.answer()
    # data = await state.get_data()
    # text = ''
    # if data["type"] == "land":
    #     text = f'<b>Новая заявка:</b>\n\n' \
    #            f'<i>Пользователь:</i> @{callback.from_user.username if callback.from_user.username else "Ник не указан"}/{callback.message.chat.id}\n' \
    #            f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
    #            f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
    #            f'<i>Направление:</i> {data["district"]}\n' \
    #            f'<i>Площадь участка:</i> {data["land_area"]} соток\n' \
    #            f'<i>Способ оплаты:</i> {data["payment_option"]}\n' \
    #            f'<i>Срок покупки:</i> {data["deadline"]}\n'
    # elif data["type"] == "house":
    #     text = f'<b>Новая заявка:</b>\n\n' \
    #            f'<i>Пользователь:</i> @{callback.from_user.username if callback.from_user.username else "Ник не указан"}/{callback.message.chat.id}\n' \
    #            f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
    #            f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
    #            f'<i>Есть участок?:</i> {data["land"]}\n' \
    #            f'<i>Направление:</i> {data["district"]}\n' \
    #            f'<i>Тип стен:</i> {data["type_wall"]}\n' \
    #            f'<i>Бюджет:</i> {data["budget"]}\n' \
    #            f'<i>Способ оплаты:</i> {data["payment_option"]}\n' \
    #            f'<i>Срок покупки:</i> {data["deadline"]}\n'
    # await bot.send_message(chat_id=config.tg_bot.channel,
    #                        text=text)


@router.callback_query(F.data.startswith('type_wall'))
@error_handler
async def get_payment_option(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем тип стен
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_payment_option {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    if answer == 'other':
        await callback.message.edit_text(text='Укажите тип материала дома?')
        await state.set_state(User.type_wall)
        return
    await state.update_data(type_wall=answer)
    await callback.message.edit_text(text='Выберите бюджет строительства, руб.',
                                     reply_markup=kb.keyboard_budget())
    await callback.answer()


@router.message(StateFilter(User.type_wall))
@error_handler
async def get_type_wall_other(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем тип стен от пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_payment_option {message.chat.id}')
    await state.update_data(type_wall=message.text)
    await state.set_state(state=None)
    await message.answer(text='Выберите бюджет строительства, руб.',
                         reply_markup=kb.keyboard_budget())


@router.callback_query(F.data.startswith('budget'))
@error_handler
async def get_payment_option(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем бюджет
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_payment_option {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    await state.update_data(budget=answer)
    await callback.message.edit_text(text='Какой вариант оплаты будете использовать?',
                                     reply_markup=kb.keyboard_payment_option())
    await callback.answer()


@router.message(or_f(F.text, F.contact), StateFilter(User.phone))
@error_handler
async def process_validate_russian_phone_number(message: Message, state: FSMContext, bot: Bot) -> None:
    """Получаем номер телефона пользователя (проводим его валидацию). Подтверждаем введенные данные"""
    logging.info("process_start_command_user")
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера. Повторите ввод, например 89991112222:")
            return
    await state.update_data(phone=phone)
    await message.answer(text='Благодарим вас за ответы, менеджер свяжется с вами в ближайшее время',
                         reply_markup=kb.keyboards_start_user())
    data = await state.get_data()
    text = ''
    if data["type"] == "sell":
        text = f'<b>Новая заявка:</b>\n\n' \
               f'<i>Пользователь:</i> @{message.from_user.username if message.from_user.username else "Ник не указан"}/{message.chat.id}\n' \
               f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
               f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
               f'<i>Номер телефона:</i> {data["phone"]}'
    else:
        if data["type"] == "flat":
            text = f'<b>Новая заявка:</b>\n\n' \
                   f'<i>Пользователь:</i> @{message.from_user.username if message.from_user.username else "Ник не указан"}/{message.chat.id}\n' \
                   f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
                   f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
                   f'<i>Номер телефона:</i> {data["phone"]}'
        elif data["type"] == "land":
            text = f'<b>Новая заявка:</b>\n\n' \
                   f'<i>Пользователь:</i> @{message.from_user.username if message.from_user.username else "Ник не указан"}/{message.chat.id}\n' \
                   f'<i>Номер телефона:</i> {data["phone"]}\n' \
                   f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
                   f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
                   f'<i>Направление:</i> {data["district"]}\n' \
                   f'<i>Площадь участка:</i> {data["land_area"]} соток\n' \
                   f'<i>Способ оплаты:</i> {data["payment_option"]}\n' \
                   f'<i>Срок покупки:</i> {data["deadline"]}\n'
        elif data["type"] == "house":
            text = f'<b>Новая заявка:</b>\n\n' \
                   f'<i>Пользователь:</i> @{message.from_user.username if message.from_user.username else "Ник не указан"}/{message.chat.id}\n' \
                   f'<i>Номер телефона:</i> {data["phone"]}\n' \
                   f'<i>Тип заявки:</i> {"Покупка" if data["payment"] == "bay" else "Продажа"}\n' \
                   f'<i>Тип недвижимости:</i> {data["type_e"]}\n' \
                   f'<i>Есть участок?:</i> {data["land"]}\n' \
                   f'<i>Направление:</i> {data["district"]}\n' \
                   f'<i>Тип стен:</i> {data["type_wall"]}\n' \
                   f'<i>Бюджет:</i> {data["budget"]}\n' \
                   f'<i>Способ оплаты:</i> {data["payment_option"]}\n' \
                   f'<i>Срок покупки:</i> {data["deadline"]}\n'
    await bot.send_message(chat_id=config.tg_bot.channel,
                           text=text)

