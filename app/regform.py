from wtforms import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    txt_username = StringField('User Name', required=True, validators=[DataRequired(),])
    txt_email = StringField('Email', required= True, validators=[Email()])
    txt_password = PasswordField('Password', required=True, validators=[DataRequired(),])
    txt_password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('txtField_password')])
    btn_submit = SubmitField('Submit')

