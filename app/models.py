from pprint import pprint
from app import db
from flask import url_for
import flask.ext.login as flask_login
from werkzeug import check_password_hash, generate_password_hash

OFFLINE = 0
ONLINE = 1
LENGTH = 240
DESC_LENGTH = 400
ACTIVE = 1
INACTIVE = 0

class Photo(db.Model):
	__tablename__ = 'photo'
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(LENGTH), index=True, unique=True)
	user_id = db.Column(db.Integer)
	name = db.Column(db.String(LENGTH))
	desc = db.Column(db.String(DESC_LENGTH))
	del_flag = db.Column(db.Integer)
	avatar_flag = db.Column(db.Integer)

	def remove(self, *args, **kwargs):
		self.del_flag = 1
		db.session.commit()

	def save(self, *args, **kwargs):
		db.session.add(self)
		db.session.commit()

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(LENGTH), index=True, unique=True)
	email = db.Column(db.String(LENGTH), index=True, unique=True)
	status = db.Column(db.SmallInteger, default=OFFLINE)
	activation = db.Column(db.SmallInteger, default=INACTIVE)
	avatar_id = db.Column(db.Integer)
	_password = db.Column('password', db.String(LENGTH), nullable=False)

	@property
	def is_active(self):
		return True

	@property
	def is_authenticated(self):
		return True
	
	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3
	
	def _get_password(self):
		return self._password

	def _set_password(self, password):
		self._password = generate_password_hash(password)
	
	password = db.synonym('_password', descriptor=property(_get_password, _set_password))

	def check_password(self, password):
		if self.password is None:
			return False
		return check_password_hash(self.password, password)

	def get_avatar(self):
		avatar = Photo.query.filter_by(id=self.avatar_id, del_flag=0, avatar_flag=1).first()
		return avatar.path

	@classmethod
	def authenticate(cls, username, password):
		the_user = cls.query.filter(User.name == username).first()

		if the_user:
			authenticated = the_user.check_password(password)
		else:
			authenticated = False

		return the_user, authenticated

	def save(self, *args, **kwargs):
		db.session.add(self)
		db.session.commit()
		
	def __repr__(self):
		return '<User %r>' % (self.name)
