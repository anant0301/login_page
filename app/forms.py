from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    txt_username = StringField('Username', validators=[DataRequired()])
    txt_password = PasswordField('Password', validators=[DataRequired()])
    btn_submit = SubmitField('Sign In')
    text_entries = ['txt_username', 'txt_password']

class RegisterForm(FlaskForm):
    txt_username = StringField('Username', validators=[DataRequired(),])
    txt_email = StringField('Email', validators=[Email()])
    txt_password = PasswordField('Password', validators=[DataRequired(),])
    btn_submit = SubmitField('Submit')
    text_entries = ['txt_username', 'txt_email', 'txt_password']

class DetailsForm(FlaskForm):
    txt_username = StringField('Username', validators=[DataRequired(),])
    txt_email = StringField('Email', validators=[Email()])
    txt_password = PasswordField('Password', validators=[DataRequired(),])
    btn_submit = SubmitField('Submit')
    text_entries = ['txt_username', 'txt_email', 'txt_password']

class DepartmentForm(FlaskForm):
    txt_did = StringField('Department ID', validators=[DataRequired()])
    txt_dname = StringField('Department Name', validators=[DataRequired()])
    txt_mid = SelectField('Manager ID', validators=[DataRequired()], default=None)
    btn_update = SubmitField('Save')
    btn_delete = SubmitField('Delete')
    text_entries = ['txt_did', 'txt_dname', 'txt_mid']

class EmployeeForm(FlaskForm):
    txt_eid = StringField('Employee ID', validators=[DataRequired()])
    txt_ename = StringField('Employee Name', validators=[DataRequired()])
    txt_salary = StringField('Salary', validators=[DataRequired()])
    txt_hra = StringField('House Rent Allowance', validators=[DataRequired()])
    txt_da = StringField('Dearness Allowance', validators=[DataRequired()])
    txt_deductions = StringField('Deductions', validators=[DataRequired()])
    txt_did = SelectField('Department ID', validators=[DataRequired()], default=None)
    btn_update = SubmitField('Save')
    btn_delete = SubmitField('Delete')
    text_entries = ['txt_eid', 'txt_ename', 'txt_salary', 'txt_hra', 'txt_da', 'txt_deductions', 'txt_did']

class ForgotPasswordForm(FlaskForm):
    txt_username = StringField('Username', validators=[DataRequired()])
    txt_email = StringField('Email', validators=[Email()])
    txt_password = PasswordField('New Password', validators= [DataRequired()])
    btn_verify = SubmitField('Verify and Update')
    text_entries = ['txt_username', 'txt_email','txt_password']