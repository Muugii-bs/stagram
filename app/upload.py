import string
import random
import time
import os
from .models import Photo
from app import app, db
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, USER_DIR_PREFIX, DEFAULT_AVATAR

class Uploader():
	def __init__(self, user, _file, _type, _name, _desc):
		self.user = user
		self.file = _file 
		self.dir = str(user.id) + '/'
		self.type = _type
		self.name = _name
		self.desc = _desc
		print self.desc, self.name

	def allowed_file(self, filename):
		return '.' in filename and \
				filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

	def upload(self):
		if self.file and self.allowed_file(self.file.filename):
			filename = self.create_name(self.file.filename)
			self.file.save(os.path.join(UPLOAD_FOLDER + self.dir, filename)) 
			if self.type == 'avatar':
				old = Photo.query.get(self.user.avatar_id)
				if not old.path == DEFAULT_AVATAR:
					old.del_flag = 1
				photo = Photo(user_id=self.user.id, path=USER_DIR_PREFIX + self.dir + filename, name=self.name, desc=self.desc, del_flag=0, avatar_flag=1)  
				photo.save()
				self.user.avatar_id = photo.id
			elif self.type == 'photo':
				photo = Photo(user_id=self.user.id, path=USER_DIR_PREFIX + self.dir + filename, name=self.name, desc=self.desc, del_flag=0, avatar_flag=0)  
				photo.save()
			db.session.commit()
			return True
		return False

	def create_name(self, filename):
		file_ext = '.' + filename.rsplit('.', 1)[1]
		rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		return self.type + '_' + str(self.user.id) + '_' + (time.strftime("%Y%m%d%H%M%S")) + '_' + rand_str + file_ext

