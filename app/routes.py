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
from .forms import DetailsForm
from .db_mongo import *

# connect to the mongo database 
from .db_mongo import Database
db_model = Database(db_name, coll_name)
db_model.user_header = user_header


@login_manager.user_loader
def load_user(id):
    return db_model.get_user(id)

@app.route('/')
### package.func()
# api 3.8
# training 3.7
# api container -> func()
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    user session already going on:
        redirect to 'emp_index'
    else:
        login page default
    '''
    if current_user.is_authenticated:
        return redirect(url_for('emp_index'))
    # login page form
    log_form = LoginForm()
    if request.method == 'POST':
        # check for user by _id=username in the collection=user
        print(log_form.txt_username.data)
        stored_user = db_model.get_user(id= str(log_form.txt_username.data))
        # if there is a user
        if stored_user:
            # password check
            if stored_user.check_password(log_form.txt_password.data):
                # correct password
                login_user(stored_user)
                return redirect(url_for('emp_index'))
            else:
                # incorrect password, correct username
                print("Incorrect password", "WARNING")
                flash("Incorrect password", "WARNING")
        # no user by the ID
        else:
            print('Invalid username')
            flash('Invalid username')
    return render_template('login.html', title='Sign In', form=log_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    user session on:
        redirect to 'emp_index'
    else:
        register page default
    '''
    if current_user.is_authenticated:
        return redirect(url_for('emp_index'))
    # register page form
    reg_form = RegisterForm()
    if request.method == 'POST':
        # add user: return True: Success
        if db_model.add_user(User(username= reg_form.txt_username.data, password= reg_form.txt_password.data, email= reg_form.txt_email.data)):
            flash('New user Registered', 'info')
        # add user fail --- user already exist
        else:
            print('User already exists', 'INFO')
            flash('User already exists', 'INFO')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form= reg_form)

@app.route('/empl')
# @login_required
def emp_index():
    # only if user login successful
    if current_user.is_authenticated:
        empl_form = EmployeeForm()
        # get department key element
        emp_table_data = db_model.get_table_data(coll_name[0], emp_header)
        # get employee data
        empl_form.txt_did.choices = db_model.get_key_data(coll_name[1], dept_header[0])
        return render_template('emplform.html', form_open='empl', table_header= emp_header, table_data= emp_table_data, form= empl_form)
    # no user session going on
    else:
        flash('Sign in required')
        return redirect(url_for('login'))

@app.route('/dept')
@login_required # login authentication done
def dep_index():
    dept_form = DepartmentForm()
    # get employee key element
    dept_table_data = db_model.get_table_data(coll_name[1], dept_header)
    # get department data
    dept_form.txt_mid.choices = db_model.get_key_data(coll_name[0], emp_header[0])
    return render_template('deptform.html', form_open='dept', table_header= dept_header, table_data= dept_table_data, form= dept_form)

@app.route('/logout')
@login_required
def logout():
    # logout from the current user session
    logout_user()
    flash("Logout successful")
    return redirect(url_for('login'))

@app.route('/update-empl', methods=['GET', 'POST'])
def update_empl():
    # update data filled in the employee form
    if request.method == 'POST':
        empl_form = EmployeeForm()
        # transform data given to collection recognised format
        emp_data = {
            emp_header[i]: request.form[header] for i, header in enumerate(empl_form.text_entries)
        }
        # Save button: update/insert
        if empl_form.btn_update.data:
            db_model.update(collection= coll_name[0], update_query= emp_data, key_header= emp_header[0], type_constr= coll_constr[coll_name[0]])
            print("Employee record updated", "INFO")
            flash("Employee record updated", "INFO")
        # Delete button: Delete 
        elif empl_form.btn_delete.data:
            db_model.delete(coll_name[0], emp_data, type_constr= coll_constr[coll_name[0]])
            print("Employee record deleted", "INFO")
            flash("Employee record deleted", "INFO")
    return redirect(url_for('emp_index'))

@app.route('/update-dept', methods=['GET', 'POST'])
def update_depl():
    # update data filled in the department form
    if request.method == 'POST':
        dept_form = DepartmentForm()
        # transform data given to collection recognised format
        dept_data = {
            dept_header[i]: request.form[header] for i, header in enumerate(dept_form.text_entries)
        }
        # Save button: update/insert
        if dept_form.btn_update.data:
            db_model.update(collection= coll_name[1], update_query= dept_data, key_header= dept_header[0], type_constr= coll_constr[coll_name[1]])
            print("Department record updated", "INFO")
            flash("Department record updated", "INFO")

        # Delete button: Delete 
        elif dept_form.btn_delete.data:
            db_model.delete(coll_name[1], dept_data, type_constr= coll_constr[coll_name[1]])
            print("Department record delelted", "INFO")
            flash("Department record delelted", "INFO")

    return redirect(url_for('dep_index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        # get user data by _id:username
        stored_user = db_model.get_user(id= str(forgot_form.txt_username.data))
        if stored_user:
            user = User(username= forgot_form.txt_username.data, email= forgot_form.txt_email.data, password= forgot_form.txt_password.data)
            # if the email and username are correct
            if user == stored_user:
                user_data = {
                    user_header[0]: user.id,
                    user_header[1]: user.email,
                    user_header[2]: user.password
                }
                db_model.update(coll_name[2], user_data, user_header[0], type_constr= coll_constr[coll_name[2]])
                print('User Password Updated')
                flash('User Password Updated')
            else:
                print('forgot_password: Incorrect User Details', 'WARNING')
                flash('Incorrect User Details', 'WARNING')
            return redirect(url_for('login'))
        else:
            print('User not Registered', 'WARNING')
            flash('User not Registered', 'WARNING')
            return redirect(url_for('register'))

    return render_template('forgot.html', title='Forgot Password', form= forgot_form)


@app.route('/details', methods=['GET', 'POST'])
@login_required
def details():
    details_form = DetailsForm()
    # initialize username and email values in the textfield
    if request.method == 'GET':
        details_form.txt_email.data = current_user.email
        details_form.txt_username.data = current_user.id
    if request.method == 'POST':
        # user object for password encryption
        user = User(username= current_user.id, email= details_form.txt_email.data, password= details_form.txt_password.data)
        user_data = {
            user_header[0]: user.id,
            user_header[1]: user.email,
            user_header[2]: user.password
        }
        db_model.update(coll_name[2], user_data, user_header[0], type_constr= coll_constr[coll_name[2]])
        # end user session and logout
        logout_user()
        print('User details updated')
        flash('User details updated')
        return redirect(url_for('login'))
    return render_template('details.html', title='Account Details', form= details_form)

@login_manager.unauthorized_handler
def unauthorized_handler():
    # unauthorized access
    return '<h1>Unauthorized!!</h1>'