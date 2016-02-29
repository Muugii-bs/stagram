from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, login_manager
from .forms import LoginForm, SignupForm
import flask.ext.login as flask_login
from .models import User
from .upload import Uploader
from .db_utils import *

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
	if not flask_login.current_user.is_authenticated:
		return render_template('home.html')
	return render_template('profile.html', 
							name=flask_login.current_user.name,
							avatar=flask_login.current_user.profile_pic)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user, authenticated = User.authenticate(form.name.data, form.password.data)
		if user and authenticated:
			if flask_login.login_user(user, remember=True):
				return redirect(url_for('index'))
		else:
			flash('Login ID or password is incorrect.', 'danger')

	return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		if not user_exist(form.name.data, form.mail.data):
			regist_user(_db=db, _name=form.name.data, _password=form.password.data, _email=form.mail.data)
			return redirect(url_for('login'))
		else:
			flash('Signup error', 'danger')
	else:
		flash('Login ID or password is incorrect.', 'danger')

	return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('index'))

@app.route('/upload/<type>', methods=['GET', 'POST'])
def upload(type):
	if not flask_login.current_user.is_authenticated:
		return render_template('home.html')
	if request.method == 'POST':
		file = request.files['avatar']
		if type == 'avatar':
			uploader = Uploader(flask_login.current_user, _file=file, _type = 'avatar')
		elif type == 'photo':
			uploader = uploader(flask_login.current_user, _file=file, _type='photo')
		else:
			flash('Upload error', 'danger')
		if uploader.upload():
			print 'ok'
		else:
			print 'upload error'
		return redirect(url_for('index'))

@app.route('/photos', methods=['POST'])
def photos():
	if not flask_login.current_user.is_authenticated:
		return jsonify({'photos': [], 'error': 'Access error!'}) 
	if request.method == 'POST' and flask_login.current_user.name == request.form['user']:
		photos = get_photos(flask_login.current_user.id)	
		return jsonify(photos)	
	else:
		return jsonify({'photos': [], 'error': 'Wrong request!'})
