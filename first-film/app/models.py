
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


films_genres = db.Table('films_genres',
    db.Column('film_id',  db.Integer, db.ForeignKey('films.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')) )


films_countries = db.Table('films_countries',
    db.Column('film_id',    db.Integer, db.ForeignKey('films.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('countries.id')) )


films_similars = db.Table('films_similars',
    db.Column('film_id',    db.Integer, db.ForeignKey('films.id')),
    db.Column('similar_id', db.Integer, db.ForeignKey('similars.id')) )


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    filmId = db.Column(db.Integer,    unique=True,  nullable=False)
    nameRu = db.Column(db.String(80), unique=False, nullable=True)
    nameEn = db.Column(db.String(80), unique=False, nullable=True)
    nameOriginal = db.Column(db.String(80), unique=False, nullable=True)

    year       = db.Column(db.Integer, unique=False, nullable=True)
    filmLength = db.Column(db.Integer, unique=False, nullable=True)

    facts     = db.relationship('Fact',    back_populates='film', lazy='dynamic')
    videos    = db.relationship('Video',   back_populates='film')
    reviews   = db.relationship('Review',  back_populates='film', lazy='dynamic')

    similars = db.relationship('Similar', lazy='dynamic')

    genres    = db.relationship('Genre',   secondary=films_genres,    back_populates='films')
    countries = db.relationship('Country', secondary=films_countries, back_populates='films')
    
    webUrl = db.Column(db.String(128), unique=False, nullable=True)

    slogan = db.Column(db.String(255), unique=False, nullable=True)
    description = db.Column(db.Text(), unique=False, nullable=True)
    shortDescription = db.Column(db.String(255), unique=False, nullable=True)

    type   = db.Column(db.String(80), unique=False, nullable=True)
    serial = db.Column(db.Boolean,    unique=False, nullable=True)

    ratingAgeLimits           = db.Column(db.String(80), unique=False, nullable=True)
    ratingKinopoisk           = db.Column(db.Float,      unique=False, nullable=True)
    ratingKinopoiskVoteCount  = db.Column(db.Integer,    unique=False, nullable=True)

    posterUrl        = db.Column(db.String(128), unique=False, nullable=True)
    posterUrlPreview = db.Column(db.String(128), unique=False, nullable=True)

    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f'Film: {self.nameRu}'


class Fact(db.Model):
    __tablename__ = 'facts'

    id = db.Column(db.Integer, primary_key=True)
    kinopoiskFilmId = db.Column(db.Integer, unique=False, nullable=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    type = db.Column(db.String(80), unique=False, nullable=True)
    spoiler = db.Column(db.Boolean, unique=False, nullable=True)

    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))

    film = db.relationship('Film', back_populates='facts', order_by=Film.id)

    def __repr__(self):
        return f'Fact: {self.kinopoiskFilmId} {self.type}'


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    kinopoiskFilmId = db.Column(db.Integer, unique=False, nullable=False)
    url = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(128), unique=False, nullable=False)
    site = db.Column(db.String(128), unique=False, nullable=False)

    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))

    film = db.relationship('Film', back_populates='videos', order_by=Film.id)

    def __repr__(self):
        return f'Video: {self.kinopoiskFilmId} {self.name}'


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    kinopoiskFilmId = db.Column(db.Integer, unique=False, nullable=False)

    kinopoiskId = db.Column(db.Integer, unique=False, nullable=True)

    type = db.Column(db.String(80), unique=False, nullable=True)
    date = db.Column(db.DateTime(timezone=True))

    positiveRating = db.Column(db.Integer, unique=False, nullable=True)
    negativeRating = db.Column(db.Integer, unique=False, nullable=True)

    author = db.Column(db.String(128), unique=False, nullable=False)
    title  = db.Column(db.String(512), unique=False, nullable=True)

    description = db.Column(db.Text, unique=False, nullable=True)

    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    film = db.relationship('Film', back_populates='reviews', order_by=Film.id)
    user = db.relationship('User', back_populates='reviews', order_by=Film.id)

    def __repr__(self):
        return f'Review: {self.kinopoiskFilmId} {self.author}'


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(80), unique=True, nullable=False)

    films = db.relationship('Film', secondary=films_genres, back_populates='genres')

    def __repr__(self):
        return f'Genre: {self.genre}'


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(80), unique=True, nullable=True)

    films = db.relationship('Film', secondary=films_countries, back_populates='countries', order_by=Film.nameRu)

    def __repr__(self):
        return f'Country: {self.country}'


class Similar(db.Model):
    __tablename__ = 'similars'

    id = db.Column(db.Integer, primary_key=True)

    similar_id = db.Column(db.Integer, unique=False, nullable=False)
    kinopoiskFilmId = db.Column(db.Integer, unique=False, nullable=False)

    nameRu = db.Column(db.String(128), unique=False, nullable=True)
    nameEn = db.Column(db.String(128), unique=False, nullable=True)
    nameOriginal = db.Column(db.String(128), unique=False, nullable=True)

    posterUrl        = db.Column(db.String(128), unique=False, nullable=True)
    posterUrlPreview = db.Column(db.String(128), unique=False, nullable=True)
    
    in_first_film = db.Column(db.Boolean, unique=False, nullable=True)

    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))
    
    def __repr__(self):
        return f'Similar: {self.kinopoiskFilmId} {self.nameRu}'


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remote_addr = db.Column(db.String(128), unique=False, nullable=True)
    path = db.Column(db.String(128), unique=False, nullable=True)
    date_time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'Request: {self.date_time}'


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name     = db.Column(db.String(80),  unique=False, nullable=True)
    email    = db.Column(db.String(80),  unique=True,  nullable=False)
    username = db.Column(db.String(80),  unique=True,  nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    role     = db.Column(db.String(32),  unique=False, nullable=False)

    reviews = db.relationship('Review',  back_populates='user')

    last_login = db.Column(db.DateTime(timezone=True), unique=False, nullable=True)

    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def is_admin(self):
        if self.role == 'admin':
            return True
        return False

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User: {self.username}'