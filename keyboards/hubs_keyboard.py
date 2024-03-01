from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import hubs


def create_hubs_keyboard(user_hubs) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for hub in hubs.keys():
        if not ((hub,) in user_hubs):
            buttons.append(InlineKeyboardButton(text=hubs[hub], callback_data=hub))

    kb_builder.row(*buttons, width=1)

    if len(user_hubs) > 0:
        kb_builder.row(InlineKeyboardButton(text='Мои хабы', callback_data='my_subscriptions'))
        kb_builder.row(InlineKeyboardButton(text='Дальше', callback_data='next'))

    return kb_builder.as_markup()


def create_user_keyboard(user_hubs) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for hub in user_hubs:
        buttons.append(InlineKeyboardButton(text=hubs[hub[0]], callback_data=hub[0]))

    kb_builder.row(*buttons, width=1)

    if 0 < len(user_hubs) < len(hubs):
        kb_builder.row(InlineKeyboardButton(text='Подписаться на хабы', callback_data='subscribe'))
        kb_builder.row(InlineKeyboardButton(text='Дальше', callback_data='next'))
    elif len(user_hubs) == 0:
        kb_builder.row(InlineKeyboardButton(text='Подписаться на хабы', callback_data='subscribe'))
    elif len(user_hubs) == len(hubs):
        kb_builder.row(InlineKeyboardButton(text='Дальше', callback_data='next'))
    return kb_builder.as_markup()


def create_subscribe_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder().row(InlineKeyboardButton(text='Подписаться на хабы', callback_data='subscribe')).as_markup()


def create_my_subscription():
    return InlineKeyboardBuilder().row(InlineKeyboardButton(text='Мои хабы', callback_data='my_subscriptions')).as_markup()



