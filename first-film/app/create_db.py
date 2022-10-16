
import re, os, json
from datetime import datetime
from .models import *


with open('json_data/films.json', 'r', encoding="utf8") as f:
    films_data = json.load(f)

with open('json_data/facts.json', 'r', encoding="utf8") as f:
    facts_data = json.load(f)

with open('json_data/videos.json', 'r', encoding="utf8") as f:
    videos_data = json.load(f)

with open('json_data/reviews.json', 'r', encoding="utf8") as f:
    reviews_data = json.load(f)

with open('json_data/similars.json', 'r', encoding="utf8") as f:
    similars_data = json.load(f)


def create_facts():
    count = 1
    for fact_data in facts_data:
        for item in fact_data['items']:
            fact = Fact(
                kinopoiskFilmId = fact_data['filmId'],
                text = item['text'],
                type = item['type'],
                spoiler = item['spoiler']
            )
            db.session.add(fact)
            # print(f'add: {count} Fact {item["type"]}')
            count += 1
    db.session.commit()

def create_videos():
    count = 1
    for video_data in videos_data:
        for item in video_data['items']:
            video = Video(
                kinopoiskFilmId = video_data['filmId'],
                url = item['url'],
                name = item['name'],
                site = item['site']
            )
            db.session.add(video)
            # print(f'add: {count} Video {item["name"]}')
            count += 1
    db.session.commit()

def create_reviews():
    count = 1
    for review_data in reviews_data:
        for item in review_data['items']:
            title = ''
            if item['title']:
                title = re.sub(r'<[^>]+>', repl='', string=item['title'], flags=re.S)
            author = ''
            if item['author']:
                author = re.sub(r'<[^>]+>', repl='', string=item['author'], flags=re.S)

            review = Review(
                kinopoiskFilmId = review_data['filmId'],
                type = item['type'],
                date = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S'),
                positiveRating = item['positiveRating'],
                negativeRating = item['negativeRating'],
                author = author,
                title  = title,
                description = item['description']
            )
            db.session.add(review)
            # print(f'add: {count} Review {item["author"]}')
            count += 1
    db.session.commit()

def create_similars():
    count = 1
    for similar_data in similars_data:
        for item in similar_data['items']:
            similar = db.session.query(Similar).filter_by(kinopoiskFilmId=item['filmId']).all()
            if not similar:
                similar = Similar(
                    similar_id = similar_data['filmId'],
                    kinopoiskFilmId = item['filmId'],
                    nameRu = item['nameRu'],
                    nameEn = item['nameEn'],
                    nameOriginal = item['nameOriginal'],
                    posterUrl = item['posterUrl'],
                    posterUrlPreview = item['posterUrlPreview']
                )
                db.session.add(similar)
                # print(f'add: {count} Similar {item["nameRu"]}')
                count += 1
            else:
                pass
            
    db.session.commit()

def create_film(film_data):
    film = Film(
        filmId = film_data['kinopoiskId'],
        nameRu = film_data['nameRu'],
        nameEn = film_data['nameEn'],
        nameOriginal = film_data['nameOriginal'],

        year = film_data['year'],
        filmLength = film_data['filmLength'],
                
        webUrl = film_data['webUrl'],

        slogan = film_data['slogan'],
        description = film_data['description'],
        shortDescription = film_data['shortDescription'],

        type = film_data['type'],
        serial = film_data['serial'],

        ratingAgeLimits = film_data['ratingAgeLimits'],
        ratingKinopoisk = film_data['ratingKinopoisk'],
        ratingKinopoiskVoteCount = film_data['ratingKinopoiskVoteCount'],

        posterUrl = film_data['posterUrl'],
        posterUrlPreview = film_data['posterUrlPreview']
    )

    return film

def create_films():
    count = 1
    for film_data in films_data:
        # if count > 10:
        #     continue
        film = create_film(film_data=film_data)

        facts = db.session.query(Fact).filter_by(kinopoiskFilmId=film.filmId).all()
        for fact in facts:
            film.facts.append(fact)
            # print(f'Film  {film.nameRu}  append:  {fact}')

        videos = db.session.query(Video).filter_by(kinopoiskFilmId=film.filmId).all()
        for video in videos:
            film.videos.append(video)
            # print(f'Film  {film.nameRu}  append:  {video}')

        reviews = db.session.query(Review).filter_by(kinopoiskFilmId=film.filmId).all()
        for review in reviews:
            film.reviews.append(review)
            # print(f'Film  {film.nameRu}  append:  {review}')
        
        similars = db.session.query(Similar).filter_by(similar_id=film.filmId).all()
        for similar in similars:
            film.similars.append(similar)
            # print(f'Film  {film.nameRu}  append:  {similar}')

        for genre in film_data['genres']:
            exists = db.session.query(Genre.genre).filter_by(genre=genre['genre']).scalar()
            if not exists:
                genre = Genre(genre=genre['genre'])
                db.session.add(genre)
                # print(f'add:  Genre  {genre}')
            else:
                genre = db.session.query(Genre).filter_by(genre=genre['genre']).scalar()
            
            film.genres.append(genre)
            # print(f'Film  {film.nameRu}  append:  {genre}')
        
        for country in film_data['countries']:
            exists = db.session.query(Country.country).filter_by(country=country['country']).scalar()
            if not exists:
                country = Country(country=country['country'])
                db.session.add(country)
                # print(f'add:  Country  {country}')
            else:
                country = db.session.query(Country).filter_by(country=country['country']).scalar()
            
            film.countries.append(country)
            # print(f'Film  {film.nameRu}  append:  {country}')

        db.session.add(film)
        
        # print(f'add:  {count}  Film  {film.nameRu}')
        count += 1

    db.session.commit()

def update_similars():
    similars = Similar.query.all()
    for similar in similars:
        film = Film.query.filter(Film.filmId==similar.kinopoiskFilmId).scalar()
        if film:
            similar.in_first_film = True
        else:
            similar.in_first_film = False
    db.session.commit()

def create_users():
    count = 1
    reviews = db.session.query(Review).all()
    for review in reviews:
        username = review.author.replace(" ", "_")
        user = db.session.query(User).filter_by(username=username).scalar()

        if not user:
            email = f'{username.lower()}@example.com'
            user = db.session.query(User).filter_by(email=email).scalar()
            if user:
                email = email.split('@')
                email = f'{email[0]}_{count}@{email[1]}'

            user = User(
                name     = review.author,
                email    = email,
                username = username,
                role     = 'user'
            )
            user.set_password(username)
            # print(f'User  {count}  add:     User    {review.author}')
    
        user.reviews.append(review)        
        db.session.add(user)

        # print(f'User  {count}  append:  Review  {review.author}  {review.kinopoiskFilmId}')
        count += 1
    db.session.commit()

def create_admins():
    admin_1 = os.environ.get('ADMIN_1')
    admin_1_pass = os.environ.get('ADMIN_1_PASS')
    if admin_1 and admin_1_pass:
        email = f'{admin_1}@example.com'
        user_1 = User(
            email    = email,
            username = admin_1,
            role     = 'admin'
        )
        user_1.set_password(admin_1_pass)
        db.session.add(user_1)
        db.session.commit()

    admin_2 = os.environ.get('ADMIN_2')
    admin_2_pass = os.environ.get('ADMIN_2_PASS')
    if admin_2 and admin_2_pass:
        email = f'{admin_2}@example.com'
        user_2 = User(
            email    = email,
            username = admin_2,
            role     = 'admin'
        )
        user_2.set_password(admin_2_pass)
        db.session.add(user_2)
        db.session.commit()

def create_all():
    db.drop_all()
    db.session.commit()

    db.create_all()
    db.session.commit()

    # create_facts()
    create_videos()
    create_reviews()
    create_similars()
    create_films()
    update_similars()
    
    create_admins()
    create_users()


if __name__ == '__main__':
    
    from app import create_app

    with create_app().app_context():
        # db.drop_all()
        # db.session.commit()
        db.create_all()
        # db.session.commit()

        # create_facts()
        # create_videos()
        # create_reviews()
        # create_similars()
        # create_films()
        # update_similars()

        # create_admins()
        # create_users()

        # print('OK')