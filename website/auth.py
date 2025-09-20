from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None

    if (login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data

        user = db.session.scalar(db.select(User).where(User.name==user_name))

        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            next_url = request.args.get('next')  # Get the URL from where the login page was accessed

            if not next_url or not next_url.startswith('/'):
                return redirect(url_for('main.index'))

            return redirect(next_url)
        else:
            flash(error)

    return render_template('user.html', form=login_form, heading='Login')

#Function for registering a new user to the site and storing it within the database
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegisterForm()

    if registration_form.validate_on_submit():
        user_name = registration_form.user_name.data
        password = registration_form.password.data
        email = registration_form.email_id.data
        contact = registration_form.contact_no.data
        address = registration_form.address.data

        user = User.query.filter_by(name=user_name).first()

        if user:
            flash('Username already exists, please try a different one')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)
        new_user = User(name=user_name, password_hash=password_hash, emailid=email, contact=contact, address=address)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=registration_form, heading='Register')


    
#Logs the user out of their account
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))