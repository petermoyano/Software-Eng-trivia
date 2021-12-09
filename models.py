from flask_sqlalchemy import SQLAlchemy



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
    password = db.Column(db.String(30), nullable=False)
    api_key = db.Column(db.String(50), nullable=False)