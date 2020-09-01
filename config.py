import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
    DATA_FILENAME = "data.json"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # max 100MB
    UPLOAD_EXTENSIONS = ['.pdf', '.zip']  # Extentions with . before
