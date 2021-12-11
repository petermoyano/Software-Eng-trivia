import os
import requests
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, flash, redirect, session, g, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
#from secrets import secret_key
from forms import NewUserForm, LoginForm, RequestQuizForm
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"
BASE_URL = "https://quizapi.io/api/v1/questions?apiKey=Fkbe9a5GDIrevApVpEzX3v5lDBWxBVDnSzyccEf1" #This is the sole endpoint available for now

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///caps1_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "MySecretKeyIsHidden123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


app.debug = DebugToolbarExtension
app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
bcrypt=Bcrypt()


@app.before_request
def add_user_to_g():
    """If we're logged in so our user is in the session, add the currnt user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user, by adding the user id to the session under the CURR_USER_KEY key"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################
# User signup/login/logout

@app.route("/")
def home():
    """Show home page"""
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def sign_up():
    """Handle user signup.    
    Create new user and add to DB. Redirect to home page.
    If validate_on_submit() does'nt validate, present form.
    If the there already is a user with that username: flash message
    and re-present form."""

    form= NewUserForm()
    if form.validate_on_submit():
        try:
            user = User(
            username = form.username.data,
            password = form.password.data,
            api_key = form.api_key.data)

            db.session.commit()
            flash("Your user has been created!")

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
            
        do_login(user) #adds the user id to the session

        return redirect("/")
    else:
        return render_template("users/signup.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    if form.validate_on_submit():
        print(bcrypt.generate_password_hash(form.password.data).decode('UTF-8'))
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/users/{user.id}")

        flash("Invalid credentials.", 'danger')
    
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("We are going to miss you! You've succesfully Loged out.")
    return redirect("/login")

##############################################################################
# General user routes:

@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def users_show(user_id):
    """Show user profile and show form to make a request for a quiz"""
    if g.user.id != user_id:
        flash("You have been redirected to your profile page")
        redirect(f"/users/{g.user.id}")

    form= RequestQuizForm()
    if form.validate_on_submit():
        params={}
        params["apiKey"] = g.user.api_key
        for fieldname, value in form.data.items():
            if fieldname != "csrf_token":
                params[fieldname] = value
        print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        print(params)
        resp = requests.get(BASE_URL, params=params)
        import pdb
        pdb.set_trace()
        return render_template("/users/show_quiz.html", resp=resp)

    return render_template("/users/quiz_form.html", form=form)
#    resp = requests.get(BASE_URL, params=params)

@app.route("/test")
def test():
    request.args
        