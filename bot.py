import os
import pandas as pd
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('API_VITAMIN_BOT'))
dp = Dispatcher(bot, storage=MemoryStorage())


class FSM_Vita(StatesGroup):
    first_element = State()
    second_element = State()

class FSM_info_Vita(StatesGroup):
    info_element = State()


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(f'Добрый день {message.from_user.full_name}')


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(f"Чтобы узнать совместимость\n"
                         f"выберите в меню /check\n"
                         f"и введите первый и второй элемент\n"
                         f"согласно названию элементов в блоке /info")


@dp.message_handler(commands=['check'], state=None)
async def start_input_first(message: types.Message):
    await FSM_Vita.first_element.set()
    await message.reply('Введите первый элемент: ')

@dp.message_handler(state=FSM_Vita.first_element)
async def start_input_second(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_element'] = message.text
    await FSM_Vita.next()
    await message.reply('Введите второй элемент: ')

@dp.message_handler(state=FSM_Vita.second_element)
async def show_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_element'] = message.text
        first_element = data['first_element']
        second_element = data['second_element']
    
    df = pd.read_csv('vita.csv', sep=',', index_col='nu')
    record = df.at[first_element, second_element]
    
    await message.answer(record)
    await state.finish()


@dp.message_handler(commands=['info'])
async def command_help(message: types.Message):


    await message.answer(f"Элементы пишем на Английском...\n"
                         f"Блок в проработке...\n")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


