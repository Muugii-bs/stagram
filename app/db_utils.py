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
from app.models import User, Photo
from datetime import timedelta
from random import randint
from config import DEFAULT_AVATAR, UPLOAD_FOLDER, USER_DIR_PREFIX
from pprint import pprint
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
	avatar = Photo(user_id=0, path=DEFAULT_AVATAR, desc='Default avatar', name='default', del_flag=0, avatar_flag=1)
	avatar.save()
	#user = User(name='user1', email='user1@gmail.com', password='password1', status=0, profile_pic=DEFAULT_AVATAR, activation=0)
	#user.save()

def regist_user(_name, _email, _password):
	avatar = Photo.query.filter_by(path=DEFAULT_AVATAR).first()
	user = User(name=_name, email=_email, password=_password, status=0, avatar_id=avatar.id, activation=0)
	user.save()
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
	res = {
		'photos': [],
		'error': ''
	}
	photos = Photo.query.filter_by(user_id=_id, del_flag=0, avatar_flag=0).all()
	for photo in photos:
		tmp = {
			'id': photo.id,
			'path': photo.path,
			'name': photo.name,
			'desc': photo.desc
		}
		res['photos'].append(tmp)
	return res

def delete_photo(id):
	photo = Photo.query.get(id)
	photo.remove()
