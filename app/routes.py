from flask_login import current_user, login_required, login_user, logout_user
from flask import flash, redirect, url_for, render_template, request
from . import *

# local file imports
from .user import User
from .forms import LoginForm
from .forms import EmployeeForm
from .forms import DepartmentForm
from .forms import RegisterForm
from .forms import ForgotPasswordForm
from .db_mongo import *

@login_manager.user_loader
def load_user(id):
    user_data = [x for x in find(coll_name[2], {'_id' : id}, {header: True for header in user_header})]
    if len(user_data) == 1:
        user_data = user_data[0]
        return User(username= user_data[user_header[0]], email= user_data[user_header[1]],\
                password= user_data[user_header[2]], encrypt_password= False)
    else:
        return None

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('emp_index'))
    log_form = LoginForm()
    if request.method == 'POST':
        stored_user = get_user(id= str(log_form.txt_username.data))
        if stored_user:
            if stored_user.check_password(log_form.txt_password.data):
                login_user(stored_user)
                return redirect(url_for('emp_index'))
            else:
                flash("Incorrect password", "WARNING")
        else:
            flash('Invalid username')
    return render_template('login.html', title='Sign In', form=log_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('emp_index'))
    reg_form = RegisterForm()
    if request.method == 'POST':
        if add_user(User(username= reg_form.txt_username.data, password= reg_form.txt_password.data, email= reg_form.txt_email.data)):
            flash('New user Registered', 'info')
        else:
            flash('User already exists', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form= reg_form)

@app.route('/empl')
# @login_required
def emp_index():
    if current_user.is_authenticated:
        empl_form = EmployeeForm()
        emp_table_data = get_table_data(coll_name[0], emp_header)
        empl_form.txt_did.choices = get_key_data(coll_name[1], dept_header[0])
        return render_template('emplform.html', form_open='empl', table_header= emp_header, table_data= emp_table_data, form= empl_form)
    else:
        flash('Sign in required')
        return redirect(url_for('login'))

@app.route('/dept')
@login_required
def dep_index():
    dept_form = DepartmentForm()
    dept_table_data = get_table_data(coll_name[1], dept_header)
    dept_form.txt_mid.choices = get_key_data(coll_name[0], emp_header[0])
    return render_template('deptform.html', form_open='dept', table_header= dept_header, table_data= dept_table_data, form= dept_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successful")
    return redirect(url_for('login'))

@app.route('/update-empl', methods=['GET', 'POST'])
def update_empl():
    if request.method == 'POST':
        empl_form = EmployeeForm()
        emp_data = {
            emp_header[i]: request.form[header] for i, header in enumerate(empl_form.text_entries)
        }
        if empl_form.btn_update.data:
            update(collection= coll_name[0], update_query= emp_data, key_header= emp_header[0], type_constr= coll_constr[coll_name[0]])
        elif empl_form.btn_delete.data:
            delete(coll_name[0], emp_data)
    return redirect(url_for('emp_index'))

@app.route('/update-dept', methods=['GET', 'POST'])
def update_depl():
    if request.method == 'POST':
        dept_form = DepartmentForm()
        dept_data = {
            dept_header[i]: request.form[header] for i, header in enumerate(dept_form.text_entries)
        }
        if dept_form.btn_update.data:
            update(collection= coll_name[1], update_query= dept_data, key_header= dept_header[0], type_constr= coll_constr[coll_name[1]])
        elif dept_form.btn_delete.data:
            delete(coll_name[1], dept_data)
    return redirect(url_for('dep_index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        stored_user = get_user(id= str(forgot_form.txt_username.data))
        if stored_user:
            user = User(username= forgot_form.txt_username.data, email= forgot_form.txt_email.data, password= forgot_form.txt_password.data)
            if user == stored_user:
                user_data = {
                    user_header[0]: forgot_form.txt_username.data,
                    user_header[1]: forgot_form.txt_email.data,
                    user_header[2]: forgot_form.txt_password.data
                }
                update(coll_name[2], user_data, user_header[0], type_constr= coll_constr[coll_name[2]])
            else:
                flash('Incorrect User Details')
                return redirect(url_for('login'))
        else:
            flash('User not Registered')
            return redirect(url_for('register'))
    return render_template('forgot.html', title='Forgot Password', form= forgot_form)


@app.route('/details', methods=['GET', 'POST'])
@login_required
def details():
    details_form = RegisterForm()
    if request.method == 'GET':
        details_form.txt_email.data = current_user.email
        details_form.txt_username.data = current_user.id
    if request.method == 'POST':
        user = User(username= current_user.id, email= details_form.txt_email.data, password= details_form.txt_password.data)
        user_data = {
            user_header[0]: user.id,
            user_header[1]: user.email,
            user_header[2]: user.password
        }
        update(coll_name[2], user_data, user_header[0], type_constr= coll_constr[coll_name[2]])
        logout_user()
        flash('Details updated')
        return redirect(url_for('login'))
    return render_template('details.html', title='Account Details', form= details_form)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return '<h1>Unauthorized!!</h1>'