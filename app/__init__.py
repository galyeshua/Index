from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import os


app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'
moment = Moment(app)


uploads_folder = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(uploads_folder):
    os.mkdir(os.path.join(app.root_path, 'static', 'uploads'))
    print('upload folder created')


from app import views_main, views_admin, models, errors
