from aiogram.dispatcher.filters.state import StatesGroup,State




class UserMessageState(StatesGroup):
    film_id = State()
    film_text = State()

    
    