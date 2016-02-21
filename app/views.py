from flask import render_template, flash, redirect, url_for, request
from app import app, db, login_manager
from .forms import LoginForm, SignupForm
import flask.ext.login as flask_login
from .models import User
from .upload import Uploader

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
		print form.name.data, form.mail.data, form.password.data
	else:
		flash('Login ID or password is incorrect.', 'danger')

	return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('index'))

@app.route('/avatar', methods=['GET', 'POST'])
def upload():
	if not flask_login.current_user.is_authenticated:
		return render_template('home.html')
	if request.method == 'POST':
		avatar = request.files['avatar']
		uploader = Uploader(flask_login.current_user, file=avatar)
		if uploader.upload():
			print 'ok'
		else:
			print 'upload error'

	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/avatar" method=post enctype=multipart/form-data>
      <p><input type=file name=avatar>
         <input type=submit value=Upload>
    </form>
    ''' 
