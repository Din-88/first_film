
from datetime import datetime
from functools import wraps
import re
from flask import abort, request
from flask_login import current_user
from flask import current_app as app
from .models import db, Request

from urllib.parse import urlparse, urljoin
from sqlalchemy import or_
from app.models import Film


# @app.before_request
def before_request():
    req = Request(
        remote_addr=request.host,
        path=request.path,
        date_time=datetime.utcnow()
    )
    db.session.add(req)
    db.session.commit()

@app.teardown_request
def teardown_request(a):
    pass


def search_film(query, search_text, limit=None):
    reg_exp = fr'{re.escape(search_text)}'

    # https://postgrespro.ru/docs/postgrespro/9.5/pgtrgm
    
    # db.session.execute('CREATE EXTENSION pg_trgm;')
    # db.session.execute('SET pg_trgm.set_limit = 0.3;')
    # db.session.execute('SET pg_trgm.similarity_threshold = 0.3;')
    # db.session.execute('SET pg_trgm.word_similarity_threshold = 0.3;')
    query = query.filter(or_(
        Film.nameRu.op("%>")(search_text),
        Film.shortDescription.op("~*")(reg_exp),
        Film.description.op("~*")(reg_exp) )
        ).order_by(Film.nameRu.op("<->>")(search_text))

    if limit:
        query = query.limit(limit)

    return query


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def admin_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        if app.config.get("LOGIN_DISABLED"):
            pass
        elif not callable(getattr(current_user, 'is_admin', None)):
            return abort(401) # Unauthorized
        elif not current_user.is_admin():
            return abort(403) # Forbidden
        return f(*args, **kwargs)
    return wrapped_view