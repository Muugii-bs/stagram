from app import db
from flask import url_for
import flask.ext.login as flask_login
from werkzeug import check_password_hash, generate_password_hash

OFFLINE = 0
ONLINE = 1
LENGTH = 120
ACTIVE = 1
INACTIVE = 0

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(LENGTH), index=True, unique=True)
	email = db.Column(db.String(LENGTH), index=True, unique=True)
	status = db.Column(db.SmallInteger, default=OFFLINE)
	activation = db.Column(db.SmallInteger, default=INACTIVE)
	profile_pic = db.Column(db.String(LENGTH))
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
