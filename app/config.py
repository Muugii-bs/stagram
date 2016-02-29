import os

MAX_CONTENT_LENGTH = 20 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/app.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'Cookpad_recruit_test_web_application_baatarsuren_munkhdorj_CHEERS20160301'
APP_DIR = os.path.abspath(os.path.dirname(__file__))
USER_DIR_PREFIX = 'static/uploads/'
UPLOAD_FOLDER = os.path.join(APP_DIR, USER_DIR_PREFIX)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
DEFAULT_AVATAR = 'static/img/default.jpg'
