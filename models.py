from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

API_KEY = "eUGtjE480cql4ZM39Ftz59nKsK6M3diNdmA5EC6Z"

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """From within app.py we import this function to connect our Flask app to our db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table"""

    __tablename__="users"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Determines how an instance of the User model is shown"""
        return f"<User #{self.id}: {self.username}>"
    
    @classmethod
    def signup(cls, username, password):
        """Sign up user. Hashes password and adds user to system"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. If such a user is authenticated, returns that
        user object, else returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False