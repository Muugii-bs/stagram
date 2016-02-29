import string
import random
import time
from app import app, db
import os
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, USER_DIR_PREFIX

class Uploader():
	def __init__(self, user, _file, _type):
		self.user = user
		self.file = _file 
		self.dir = str(user.id) + '/'
		self.type = _type

	def allowed_file(self, filename):
		return '.' in filename and \
				filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

	def upload(self):
		if self.file and self.allowed_file(self.file.filename):
			filename = self.create_name(self.file.filename)
			self.file.save(os.path.join(UPLOAD_FOLDER + self.dir, filename))
			if self.type == 'avatar':
				self.user.profile_pic = USER_DIR_PREFIX + self.dir + filename
			db.session.commit()
			return True
		return False

	def create_name(self, filename):
		file_ext = '.' + filename.rsplit('.', 1)[1]
		rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		return self.type + '_' + str(self.user.id) + '_' + (time.strftime("%Y%m%d%H%M%S")) + '_' + rand_str + file_ext

