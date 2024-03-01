from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, Text

from lexicon.lexicon import hubs, description
from database.database import DataBase
from keyboards.hubs_keyboard import create_hubs_keyboard, create_user_keyboard, create_subscribe_keyboard, create_my_subscription


db = DataBase("database/db2.db")

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if not (db.users_exist(message.from_user.id)):
        db.add_user(message.from_user.id)
    if len(db.get_subscribtions(message.from_user.id)):
        keyboard = create_my_subscription()
        await message.answer(text="Нажми, чтобы увидеть хабы на которые ты подписан.", reply_markup=keyboard)
    elif len(db.get_subscribtions(message.from_user.id)) == 0:
        keyboard = create_subscribe_keyboard()
        await message.answer(text="Выбери интересующие тебя <b>хабы</b>, а вечером бот пришлет тебе лучшие статьи <b>дня</b>, по выбранным тобой темам. Каждое <b>воскресенье</b> приходит подборка лучших статей за неделю.\nВыбирай скорее хабы и погружайся в волшебный мир технологий!", reply_markup=keyboard)


@router.callback_query(Text(text=[*hubs, 'subscribe']))
async def process_add_del_subscribe_command(callback: CallbackQuery):
    if not ((callback.data,) in db.get_subscribtions(callback.from_user.id)):

        if callback.data != 'subscribe':
            db.add_subscribtions(callback.from_user.id, callback.data)

        keyboard = create_hubs_keyboard(db.get_subscribtions(callback.from_user.id))

        if len(keyboard.__dict__['inline_keyboard']) == 2:
            await callback.message.edit_text(text='Вот это любознательность!', reply_markup=keyboard)
            await callback.answer(text=None if callback.data == 'subscribe' else description[callback.data])
        else:
            await callback.message.edit_text(text='Выбери интересующие тебя хабы.', reply_markup=keyboard)
            await callback.answer(text=None if callback.data == 'subscribe' else description[callback.data])
    else:
        db.del_subscribtions(callback.from_user.id, callback.data)

        keyboard = create_user_keyboard(db.get_subscribtions(callback.from_user.id))
        keyboard2 = create_subscribe_keyboard()

        if len(keyboard.__dict__['inline_keyboard']) == 1:
            await callback.message.edit_text(text='Больше нечего удалять, подпишись на хабы.', reply_markup=keyboard2)
            await callback.answer(text=None if callback.data == "subscribe" else f'Ты отписался от хаба "{hubs[callback.data]}"')
        else:
            await callback.message.edit_text(text='Твои хабы. Нажми, чтобы удалить.', reply_markup=keyboard)
            await callback.answer(text=None if callback.data == "subscribe" else f'Ты отписался от хаба "{hubs[callback.data]}"')


@router.callback_query(Text(text="my_subscriptions"))
async def process_get_my_subscribes_command(callback: CallbackQuery):
    keyboard = create_user_keyboard(db.get_subscribtions(callback.from_user.id))

    await callback.message.edit_text("Твои хабы. Нажми, чтобы удалить.", reply_markup=keyboard)
    await callback.answer(text="Твои подписки")


@router.callback_query(Text(text="next"))
async def process_next_command(callback: CallbackQuery):
    keyboard = create_my_subscription()
    await callback.message.edit_text(text="Отлично! Теперь каждый день бот будет радовать тебя интересными статьями!", reply_markup=keyboard)
    await callback.answer(text="Жди новые статьи ;)")


@router.callback_query(Text(text="subscribe"))
async def process_subscribe_command(callback: CallbackQuery):
    await callback.message.edit_text(text="Выбери интересующие тебя хабы.", reply_markup=create_hubs_keyboard(db.get_subscribtions(callback.from_user.id)))
    await callback.answer(text=None)


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    if len(db.get_subscribtions(message.from_user.id)):
        keyboard = create_my_subscription()
        await message.answer(text="Это бот, который делает <b>ежедневную</b> и <b>еженедельную</b> рассылку со статьями с сайта https://habr.com/\nВыбери интересующие тебя <b>хабы</b>, а вечером бот пришлет тебе лучшие статьи <b>дня</b>, по выбранным тобой темам. Каждое <b>воскресенье</b> приходит подборка лучших статей за неделю.\nКаждый день рассылка в <b>восемь вечера</b> по мск\nВыбери интересные тебя темы или отпишись от ненужных", reply_markup=keyboard)
    else:
        keyboard = create_subscribe_keyboard()
        await message.answer(text="Это бот, который делает <b>ежедневную</b> и <b>еженедельную</b> рассылку со статьями с сайта https://habr.com/\nВыбери интересующие тебя <b>хабы</b>, а вечером бот пришлет тебе лучшие статьи <b>дня</b>, по выбранным тобой темам. Каждое <b>воскресенье</b> приходит подборка лучших статей за неделю.\nКаждый день рассылка в <b>восемь вечера</b> по мск\nВыбери интересные тебя темы или отпишись от ненужных", reply_markup=keyboard)


