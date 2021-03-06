from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, TextField
from wtforms.validators import DataRequired

class LoginForm(Form):
	name = TextField(u'username', validators=[DataRequired()])
	password = PasswordField(u'password', validators=[DataRequired()])
	submit = SubmitField(u'login')


