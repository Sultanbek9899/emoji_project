from unicodedata import category
from aiogram import types
from database.manager import CategoryManager, FilmManager, GuessedFilmManager

from bot_utils.keyboards import get_category_btns
from redis_client import redis_client
from .states import UserMessageState
from aiogram.dispatcher import FSMContext 

def get_random_film(tg_id, category):
    guessed_film = GuessedFilmManager().get_guessed_films_ids(tg_id)
    film = FilmManager().get_random_film(film_ids=guessed_film, category_id=category)
    return  film


async def welcome_message(message:types.Message):
    text = """
        Привет. это бот для игры в угадай фильм по эмоджи.
        Чтобы начать игру, отправь мне команду /start_game
    """
    await message.answer(text)


async def start_game(message:types.Message): 
    text="Выберите категорию игры: "
    user_id = message["from"].id
    data = await redis_client.get_user_data(user_id)
    if data:
        await message.answer("У вас уже имеется текущая игра. Желаете завершить игру ?")
    else:
        markup = get_category_btns()
        await message.answer(text, reply_markup=markup)



async def start_with_category(call: types.CallbackQuery, state: FSMContext ):
    user_data = await redis_client.get_user_data(call.message.chat.id)
    if user_data:
        text = """
            У вас имеется активная игра, завершите игру, 
            чтобы выбрать новую категорию.
        """
        await call.message.answer(text)
    else:
        choice = str(call.data).split("_")[1]
        data = {
            "level_choice": choice,
            "test":"test",
        }
        user_id = call.message.chat.id
        await redis_client.cache_user_data(user_tg_id=user_id, data=data)
        tg_id = user_id
        guessed_film = GuessedFilmManager().get_guessed_films_ids(tg_id)
        film = FilmManager().get_random_film(film_ids=guessed_film, category_id=choice)
        
        await redis_client.cache_user_film(tg_id, {"id":film.id, "text":film.name_text})

        await call.message.answer("Вы выбрали категорию. Игра началась...")
        await call.message.answer(f"{film.emoji_text}")


async def send_questions(message:types.Message, state: FSMContext):
    tg_id = message["from"].id
    user_data = await redis_client.get_user_data(tg_id)
    if user_data:
        answer = message.text
        user_film = await redis_client.get_user_film(tg_id)
        print(user_film)
        if answer == user_film["text"]:
            await message.answer(f"Ура, вы угадали название фильма {user_film['text']}")
            await redis_client.delete_user_film(tg_id)
            GuessedFilmManager().insert_guessed_film(tg_user_id=tg_id, film_id=user_film["id"])
            film = get_random_film(tg_id, category=user_data["level_choice"])
            await redis_client.cache_user_film(tg_id, {"id":film.id, "text":film.name_text})
            await message.answer("Угадай следующий фильм: ")
            await message.answer(f"{film.emoji_text}")
        else:
            await message.answer("Вы не угадали название, попробуйте ещё раз написать.")
    else:
        text = "У вас нету активной игры. Напишите /start_game для начало новой игры"
        await message.answer(text)



async def finish_game(message:types.Message):
    user_id = message["from"].id
    print(user_id)
    await redis_client.del_user_data(user_id)
    await message.answer("Игра завершена!")
    await message.answer("Количество угаданных фильмов: 0")



async def get_movie(message:types.Message):
    films = FilmManager().get_films()
    for f in films:
        await message.answer(f"{f.emoji_text}")















