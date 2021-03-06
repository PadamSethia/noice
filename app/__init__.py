import logging
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config
from werkzeug.debug import DebuggedApplication
from flask_marshmallow import Marshmallow
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    ma.init_app(app)

    sentry_sdk.init(
        dsn="https://8bbfa12b1e3247699d7f6f4d7ec6aaca@sentry.io/1852554",
        integrations=[FlaskIntegration()]
    )
    
    with app.app_context():
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.main import bp as main_bp
        app.register_blueprint(main_bp, url_prefix='/')

        from app.basic_master import bp as basic_master_bp
        app.register_blueprint(basic_master_bp, url_prefix='/basic_master')

        from app.main_master import bp as main_master_bp
        app.register_blueprint(main_master_bp, url_prefix='/main_master')
        
        from app.transaction import bp as transaction_bp
        app.register_blueprint(transaction_bp, url_prefix='/transaction')

        from app.reports import bp as reports_bp
        app.register_blueprint(reports_bp, url_prefix='/reports')
        
        from app.production import bp as production_bp
        app.register_blueprint(production_bp, url_prefix='/production')

        # from app.employee import bp as emp_bp
        # app.register_blueprint(emp_bp, url_prefix='/employee')

        # from app.transaction import bp as trans_bp
        # app.register_blueprint(trans_bp, url_prefix='/transaction')

        
       
        db.create_all()

        from app.model import Role
        if Role(name="ADMIN").query.first():
            pass
        else:

            db.session.add(Role(name='ADMIN'))
            db.session.commit()
    return app
