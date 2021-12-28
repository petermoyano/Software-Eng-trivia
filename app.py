import os
import requests
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, flash, redirect, session, g, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
#from secrets import secret_key
from forms import NewUserForm, LoginForm, RequestQuizForm
from sqlalchemy.exc import IntegrityError
from functions import ques_number, analize_answers, give_score
from models import API_KEY


CURR_USER_KEY = "curr_user"
BASE_URL = "https://quizapi.io/api/v1/questions" #This is the sole endpoint available for now



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
    """If we're logged in add the current user to Flask global,so our user is in the session"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        g.user.api_key = API_KEY
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
            username = form.username.data
            password = form.password.data
            user = User.signup(username, password)
            db.session.add(user)
            db.session.commit()
            flash(f"Thanks for signing up!, {user.username}. You can now take a quiz!")
            do_login(user)
            return redirect(f"/users/{user.id}")
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
def show_and_handle_quiz(user_id):
    """Show user profile and show form to make a request for a quiz"""
    if g.user.id != user_id:
        flash("You have been redirected to your profile page", "warning")
        redirect(f"/users/{g.user.id}")

    form= RequestQuizForm()
    if form.validate_on_submit():
        payload={}
        payload["apiKey"] = g.user.api_key
        for fieldname, value in form.data.items():
            if (fieldname != "csrf_token"):
                if(value != None):
                    payload[fieldname] = value
        resp = requests.post(BASE_URL, json=payload)
        jsonr = resp.json()
        session["jsonr"] = jsonr

        """ The following is defined to give each radio button a label-input assosiacion with an individual id 
        dynamically generated based on the place they hold in the answers for that particular question, and
        discarting answers with the value of None
        iter_base -> [['foo', 'bar', 'baz foo'], ['foo bar', ... , ], [..., , ,] ...]
        """
        iter_base = analize_answers(jsonr)
        session["iter_base"] = iter_base
        return render_template("/users/show_quiz.html", jsonr=jsonr, ques_number=ques_number, iter_base=iter_base)

    return render_template("/users/quiz_form.html", form=form)

@app.route('/users/<int:user_id>/calculate_score', methods=["POST"])
def handle_quiz_results(user_id):
    """Handle form submission and compare answers to give a score"""
    jsonr = session["jsonr"]
    user_responses = []
    for question in jsonr:        
        user_resp = request.form[f"input-group {ques_number[jsonr.index(question) + 1]}"]
        user_responses.append(user_resp)
    session["user_responses"] = user_responses

    score = give_score(jsonr, user_responses)
    session["score"] = score

    flash(f"Your score was {score}%!")

    return redirect(f"/users/{g.user.id}/show_results")

@app.route('/users/<int:user_id>/show_results')
def show_quiz_results(user_id):
    jsonr = session["jsonr"]
    iter_base = session["iter_base"]
    score = session["score"]
    user_responses = session["user_responses"]
    return render_template("/users/show_results.html", jsonr=jsonr, ques_number=ques_number, iter_base=iter_base, score=score, user_responses=user_responses)

    
##############################################################################
# Nav routes:
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/api')
def api():
    return render_template("api.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")
        