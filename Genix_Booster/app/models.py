from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(6))
    password = db.Column(db.String(200))

    def __repr__(self):
        return'<User id {},name{}>'.format(self.id,self.name)
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    price = db.Column(db.NUMERIC(10,2))
    compare_price = db.Column(db.NUMERIC(10,2))
    description = db.Column(db.Text)
    pictures = db.Column(db.Text)
    category = db.Column(db.String(200))
    added = db.Column(db.DateTime,default=datetime.datetime.now())
class Watch(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1500))
    group = db.Column(db.String(1500))

class Report(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(1500))
    message = db.Column(db.String(1500))


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(1500))
    message = db.Column(db.String(1500))

class Advert(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(1500))
    message = db.Column(db.String(1500))

    

    

