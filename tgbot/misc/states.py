from aiogram.dispatcher.filters.state import StatesGroup, State



class CharacterState(StatesGroup):

    initial = State()
    conversation = State()