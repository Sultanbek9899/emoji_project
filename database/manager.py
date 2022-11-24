from database.models import Category, Film, UserGuessedFilm
from db import get_session


class CategoryManager():
    def __init__(self):
        self.model = Category
        self.session = get_session()

    def insert_category(self, data):
        inserts = []
        for c in data:
            inserts.append(
                Category(
                    name=c[0]
                )
            )
        self.session.add_all(inserts)
        self.session.commit()

    def get_all_categories(self):
        results = self.session.query(self.model).all()
        return results


class FilmManager():

    def __init__(self):
        self.session = get_session()
        self.model = Film
    

    def insert_film(self, data):
        inserts = []
        for film in data:
            inserts.append(
                Film(
                    emoji_text=film[0],
                    name_text=film[1],
                    category=film[2]
                )
            )
        self.session.add_all(inserts)
        self.session.commit()

    def get_random_film(self, film_ids, category_id=None):
        from sqlalchemy import not_
        from sqlalchemy.sql import func
        if category_id:
            q = self.session.query(self.model).filter(
                not_(Film.id.in_(film_ids)),
                Film.category==category_id,
            ).order_by(func.rand()).first()
            return q
        else:
            q = self.session.query(self.model).filter(
                not_(Film.id.in_(film_ids)),
            ).order_by(func.rand()).first()
            return q


        

class GuessedFilmManager():


    def __init__(self):
        self.session = get_session()
        self.model = UserGuessedFilm
        
    def insert_guessed_film(self, tg_user_id, film_id):
        insert = UserGuessedFilm(
            tg_user_id = tg_user_id,
            film = film_id
        )
        self.session.add(insert)
        self.session.commit()        

    def get_guessed_films_ids(self, tg_user_id):
        ids=self.session.query(UserGuessedFilm.film).filter(
            UserGuessedFilm.tg_user_id==tg_user_id
        )
        return ids


