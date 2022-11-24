from unittest import skip
from aiogram import executor
from sys import argv
from init_db import create_tables
from utils import fill_category_data, fill_films_data
from bot_router import dp

if __name__ == "__main__":
    data = argv
    print(data)
    if data[1] == "migrate":       
        create_tables()
        print("Все таблицы созданы!")

    elif data[1] == "runbot":
        print("Бот запущен...")    
        executor.start_polling(dp, skip_updates=True)

    elif data[1] == "fill_category":
        fill_category_data("data_files/category_data.csv")
        print("Перенос данных завершен.")
    elif data[1] == "fill_films":
        fill_films_data()
        print("Перенос фильмов в базу завершен.")
    else: 
        print("Напишите определенную команду!!!")