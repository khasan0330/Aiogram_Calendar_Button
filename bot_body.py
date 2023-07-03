from keyboards import generate_calendar_button

from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message, CallbackQuery

from aiogram_calendar import simple_cal_callback, SimpleCalendar

import os
from dotenv import load_dotenv

import datetime
from datetime import timezone

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer(
        text='Добро пожаловать, для брони комнаты выберите дату',
        reply_markup=generate_calendar_button()
    )


@dp.message_handler(lambda message: 'Выбрать дату 📆' in message.text)
async def call_calendar(message: Message):
    """Реакция на кнопку с текстом <Выбрать дату> """
    await message.answer(
        text="Нажмите на интересующую дату: ",
        reply_markup=await SimpleCalendar().start_calendar()
    )


@dp.callback_query_handler(simple_cal_callback.filter())
async def select_date_day(call: CallbackQuery, callback_data: dict):
    """Реакция на нажатия даты"""
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    year, month, day = date.strftime("%Y %m %d").split()
    dt = datetime.datetime(int(year), int(month), int(day))
    unix_time = int(dt.replace(tzinfo=timezone.utc).timestamp())

    if selected:
        """Если дата выбрана"""
        await call.message.answer(
            text=f'Вы выбрали дату: {date.strftime("%d/%m/%Y")}, '
                 f'\nДля удобной записи в ДБ используйте UnixTime: {unix_time}',
            reply_markup=generate_calendar_button()
        )
    else:
        """Если дата не выбрана"""
        await bot.delete_message(
            chat_id=call.from_user.id,
            message_id=call.message.message_id  # Зацикливаем если нужно
        )
        await call.message.answer(
            text='Вы не выбрали дату',
            reply_markup=generate_calendar_button()  # Зацикливаем если нужно
        )


if __name__ == '__main__':
    executor.start_polling(dp)
