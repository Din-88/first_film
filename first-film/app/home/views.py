
from flask import render_template, request
from flask import current_app as app

import datetime

from collections import OrderedDict

from . import home
from .. forms import SearchForm
from .. models import db, Film, Genre, Review
from .. utils import search_film


@home.route('/')
@home.route('/<type>')
def index(type=''):
    films_per_page = app.config["FILMS_PER_PAGE"]

    page = request.args.get(key='page', default=1, type=int)
    genre = request.args.get('genre', default=None, type=str)

    params = {}
    query = db.session.query(Film)

    if type:
        params['type'] = type
        if type == 'films':
            params['film_type'] = 'film'
            query = query.filter(Film.type=='FILM')
        elif type == 'series':
            params['film_type'] = 'serial'
            query = query.filter(Film.type=='TV_SERIES')
        elif type == 'mini_series':
            params['film_type'] = 'mini_serial'
            query = query.filter(Film.type=='MINI_SERIES')
        elif type == 'cartoons':
            params['film_type'] = 'cartoons'
            query = query.filter(Film.genres.any(Genre.genre=='мультфильм'))
        elif type == 'new':
            params['film_type'] = 'new'
            years_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).year
            query = query.filter(db.cast(Film.year, db.Integer) >= years_ago)

    if genre:
        params['genre'] = genre
        query = query.filter(Film.genres.any(Genre.genre==genre))

    paginate = query.paginate(page=page, per_page=films_per_page, error_out=False) 

    return render_template('index.html', films=paginate.items, params=params, paginate=paginate, paginate_url='home.index')


@home.route('/search/<int:page>', methods=['GET', 'POST'])
@home.route('/search', methods=['GET', 'POST'])
def search(page=1, search_text='а'):
    search_text = request.form.get(key='search_text', default='a', type=str)
    
    if request.method == 'POST':
        found = search_film(query=Film.query, search_text=search_text, limit=100).all()
        return render_template('search_result.html', found=found, search_text=search_text)

    films_per_page = app.config["FILMS_PER_PAGE"]
    params = {'search_text': search_text}
    query = search_film(query=Film.query, search_text=search_text)
    paginate = query.paginate(page=page, per_page=films_per_page, error_out=False)

    return render_template('index.html', films=paginate.items, paginate=paginate, paginate_url='home.search', params=params)


@home.route('/second_nav/<type>')
def second_nav(type):
    query = db.session.query(Genre.genre).join(Genre.films)

    if type == 'films':
        query = query.filter(Film.type=='FILM')
    elif type == 'series':
        query = query.filter(Film.type=='TV_SERIES')
    elif type == 'mini_series':
        query = query.filter(Film.type=='MINI_SERIES')
    elif type == 'cartoons':
        # query = query.filter(Film.genres.contains(Genre.query.filter(Genre.genre=='мультфильм').first()))
        query = query.filter(Film.genres.any(Genre.genre=='мультфильм'))
    elif type == 'new':
        years_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).year
        query = query.filter(db.cast(Film.year, db.Integer) >= years_ago)

    genres = query.group_by(Genre.genre).all()
    genres = [genre.genre for genre in genres]

    return render_template('second_nav_sub.html', type=type, genres=genres)


@home.route('/<int:film_id>')
@home.route('/<film_type>/<int:film_id>')
def film_page(film_type=None, film_id=None):
    a = film_type
    film = db.session.query(Film).filter(Film.filmId==film_id).one()
    reviews = film.reviews.limit(5).all()
    similars = film.similars.limit(6).all()

    film = db.session.query(Film).filter(Film.filmId==film_id).one()

    videos = OrderedDict()
    for video in film.videos:
        if video.site == 'YOUTUBE':
            you_tube_id = video.url[-11:]
            # url = f'https://www.youtube.com/embed/{youTube_id}?controls=0'
            url = f'https://www.youtube-nocookie.com/embed/{you_tube_id}?controls=1'

            video_type = ''
            if video.name.startswith('Тизер'):
                video_type = 'teaser'
            elif video.name.startswith('Промо'):
                video_type = 'promo'
            elif video.name.startswith('Трейлер'):
                video_type = 'trailer'
            elif video.name.startswith('О '): # 'О съемках'
                video_type = 'about'
            else:
                video_type = 'other'

            if video_type not in videos:
                videos[video_type] = []

            videos[video_type].append({
                                'id': video.id,
                                'kinopoiskFilmId': video.kinopoiskFilmId,
                                'url': url,
                                'name': video.name,
                                'site': video.site})
                 
    return render_template('film.html', film=film, videos=videos, reviews=reviews, similars=similars)


@home.route('/more_reviews/<int:film_id>/<int:review_page>')
def more_reviews(film_id, review_page):
    offset = 5 + (review_page * 5)
    reviews = Review.query.filter(Review.kinopoiskFilmId==film_id).limit(5).offset(offset).all()

    return render_template('reviews.html', reviews=reviews)


@home.route('/about')
def about():
    return render_template('about.html')

@home.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')
