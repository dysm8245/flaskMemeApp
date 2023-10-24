from flask import Blueprint, render_template, request, redirect
from forms import UserLoginForm, UserSignupForm
from models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserSignupForm()

    try:
        #making sure form is correct
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            #creating user to store to database
            user = User(first_name, last_name, email, username, password)
            #sending user to database
            db.session.add(user)
            db.session.commit()
            #printing confirmation in terminal
            print('User added to database')
            return redirect("/signin")
    except:
        raise Exception('Invalid form data')
    
    return render_template('signup.html', form=form)

@auth.route('/signin', methods=["GET", "POST"])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            #checking if user with username submitted exists and if so if they're password is correct
            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                #log in user
                login_user(logged_user)
                print('Succesfful login')
                return redirect("/profile")
            else:
                print("We weren't able to log in this user")
    except:
        raise Exception('Invalid form data')
    
    return render_template('signin.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect("/signin")