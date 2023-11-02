from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dsjfkheiw3287yfdjs3wr2yfdsk3'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .customerView import customerView
    from .adminView import adminView
    from .kioskView import kioskView
    from .retailerView import retailerView

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(customerView, url_prefix='/')
    app.register_blueprint(adminView, url_prefix='/')
    app.register_blueprint(kioskView, url_prefix='/')
    app.register_blueprint(retailerView, url_prefix='/')

    from .models import Beer

    with app.app_context():
        db.create_all()

    return app
