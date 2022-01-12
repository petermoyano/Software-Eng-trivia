from models import db, User
from flask_bcrypt import Bcrypt
from app import app
bcrypt=Bcrypt()
"""api_key1 = "Fkbe9a5GDIrevApVpEzX3v5lDBWxBVDnSzyccEf1"
    api_key2 = "eUGtjE480cql4ZM39Ftz59nKsK6M3diNdmA5EC6Z"  """


db.drop_all()
db.create_all()

def seed_users():
    test_user = User(username="test_user", 
        password= bcrypt.generate_password_hash("test_user").decode('UTF-8')) 

    user2 = User(username="user2", 
        password= bcrypt.generate_password_hash("user2").decode('UTF-8'))

    db.session.add(test_user)
    db.session.add(user2)
    db.session.commit()
seed_users()