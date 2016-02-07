import string
import random
import time
from app import app, db
import os

app_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(app_dir, 'static/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

class Uploader():
	def __init__(self, user, file):
		self.user = user
		self.file = file 

	def allowed_file(self, filename):
		return '.' in filename and \
				filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

	def upload(self):
		if self.file and self.allowed_file(self.file.filename):
			filename = self.create_name(self.file.filename)
			self.file.save(os.path.join(UPLOAD_FOLDER, filename))
			self.user.profile_pic = 'static/uploads/' + filename
			db.session.commit()
			return True
		return False

	def create_name(self, filename):
		file_ext = '.' + filename.rsplit('.', 1)[1]
		rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		return 'avatar_' + self.user.name + '_' + (time.strftime("%Y%m%d%H%M%S")) + '_' + rand_str + file_ext

