from models import db, User
from app import app

db.drop_all()
db.create_all()

user1 = User(username="user1", password="user1", api_key = "Fkbe9a5GDIrevApVpEzX3v5lDBWxBVDnSzyccEf1" )

db.session.add(user1)
db.session.commit()