from models import db, User
from flask_bcrypt import Bcrypt
from app import app
bcrypt=Bcrypt()

db.drop_all()
db.create_all()
def seed_users():
    user1 = User(username="user1", 
        password= bcrypt.generate_password_hash("user1").decode('UTF-8'), 
        api_key = "Fkbe9a5GDIrevApVpEzX3v5lDBWxBVDnSzyccEf1")

    db.session.add(user1)
    db.session.commit()
seed_users()