from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length

class NewUserForm(FlaskForm):
    """New User form"""
    username = StringField("Enter your username!", validators=[DataRequired()])
    password = PasswordField("Just let Chrome make a password for you", validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RequestQuizForm(FlaskForm):
    """Get parameters to create request to API"""
    category = SelectField('Choose your destiny : ', choices=[("linux", "Linux"),
    ("bash", "Bash"),
    ("php", "PHP"),
    ("html", "HTML"),
    ("wordpress", "WordPress"),
    ("laravel", "Laravel"),
    ("kubernetes", "Kubernetes"),
    ("docker", "Docker"),
    ("mysql","MySql"),
    ("cms", "CMS"),
    ("code", "Code"),
    ("devops", "DevOps"),
    ("", "Uncategorized")])
    difficulty = SelectField('Choose your pain : ', choices=[("Easy", "Easy"), ("medium", "Medium"), ("hard", "Hard"), ("", "None")])
    limit=SelectField('Choose the length of your suffering : ', choices=[('1', '1'), ('5', '5'), ('10', '10'), ("", "None")])


