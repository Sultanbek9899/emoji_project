from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    BigInteger, 
    UnicodeText,
    Text,
    ForeignKey,
    null,

)
from db import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True, 
        unique=True
        )
    name = Column(String(100), nullable=False)


class Film(Base):
    __tablename__ = "film"
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True, 
        unique=True
        )
    emoji_text = Column(UnicodeText, nullable=False)
    name_text = Column(Text, nullable=False)
    category = Column(Integer, ForeignKey("category.id"), nullable=False)



class UserGuessedFilm(Base):
    __tablename__ = "user_guessed_film"
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True, 
        unique=True
        )
    tg_user_id = Column(String(50), nullable=False)
    film = Column(Integer, ForeignKey("film.id"), nullable=False)

