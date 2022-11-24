import csv
from database.manager import CategoryManager,FilmManager



def fill_category_data(filename):
    # Для заполнения базы данными.
    with open(filename, "r", encoding="utf-8") as csv_file:
        rows = csv.reader(csv_file, delimiter=",")
        CategoryManager().insert_category(rows)


def fill_films_data():
    with open("data_files/emojies.csv", "r", encoding="utf-8") as file:
        rows = csv.reader(file, delimiter=",")
        FilmManager().insert_film(data=rows)
    
