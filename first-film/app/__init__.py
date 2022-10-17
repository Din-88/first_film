
from datetime import datetime
from flask import Flask, request
from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy


from config import DevelopmentConfig, ProductionConfig

from . forms import *
from . models import *

from . create_db import create_all

def create_app():
    app = Flask(__name__)
    
    with app.app_context():
        app.config.from_object(ProductionConfig)
        db.init_app(app)

        # https://postgrespro.ru/docs/postgrespro/9.5/pgtrgm
        # try:
        #     db.session.execute('CREATE EXTENSION pg_trgm;')
        #     db.session.execute('SET pg_trgm.set_limit = 0.3;')
        #     db.session.execute('SET pg_trgm.similarity_threshold = 0.3;')
        #     db.session.execute('SET pg_trgm.word_similarity_threshold = 0.3;')
        # except:
        #     pass

        if app.config['CREATE_DB']:
            create_all()


        from . home import home as home_blueprint
        from . admin import admin as admin_blueprint
        app.register_blueprint(home_blueprint,  url_prefix='/')
        app.register_blueprint(admin_blueprint, url_prefix='/admin')

        from . home import login_manager
        login_manager.init_app(app)
       
        from . utils import before_request, teardown_request
        app.before_request_funcs = {None:[before_request]}
         
        from . error_views import unauthorized, forbidden, page_not_found
        app.register_error_handler(401, unauthorized)
        app.register_error_handler(403, forbidden)
        app.register_error_handler(404, page_not_found)

        return app


if __name__ == '__main__':
    app = create_app()
    app.run()