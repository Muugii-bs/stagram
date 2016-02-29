from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
    )
from app import app
from app.models import User
from datetime import timedelta
from random import randint
from config import DEFAULT_AVATAR, UPLOAD_FOLDER, USER_DIR_PREFIX
import math
import os

def db_clean():

    engine = create_engine('sqlite:////tmp/app.db')

    conn = engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
                fks.append(
                    ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


def db_create_default(db):
	user = User(name='user1', email='user1@gmail.com', password='password1', status=0, profile_pic=DEFAULT_AVATAR, activation=0)
	db.session.add(user)
	db.session.commit()

def regist_user(_db, _name, _email, _password):
	user = User(name=_name, email=_email, password=_password, status=0, profile_pic=DEFAULT_AVATAR, activation=0)
	_db.session.add(user)
	_db.session.commit()
	user = User.query.filter_by(name=_name, email=_email).first()
	print UPLOAD_FOLDER + str(user.id)
	if not os.path.exists(UPLOAD_FOLDER + str(user.id)):
		os.makedirs(UPLOAD_FOLDER + str(user.id))
		print 'ok'

def user_exist(_name, _email):
	user = User.query.filter_by(name=_name, email=_email).first()
	if user is None:
		return False
	else:
		return True

def get_photos(_id):
	user_dir = UPLOAD_FOLDER + str(_id) 
	send_dir = USER_DIR_PREFIX + str(_id) + '/'
	res = {
		'photos': [],
		'error': ''
	}
	if os.path.exists(user_dir):
		for subdir, dirs, files in os.walk(user_dir):
			for file in files:
				if file.startswith('photo_' + str(_id)):
					res['photos'].append(send_dir + file)
	else:
		res['error'] = 'User directory not found!'
	return res

