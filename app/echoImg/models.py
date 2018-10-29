# from exts import db
from app.echoImg.exts import db


class User(db.Model):
    __tablename__ = 'user'
    telephone = db.Column(db.String(11), nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    true_name = db.Column(db.String(50))
    # sex = db.Column(db.String(10))
    # birthday = db.Column(db.String(50))
    email = db.Column(db.String(50))


#
# class Super_admin(db.Model):
#     __tablename__ = 'superadmin'
#     username = db.Column(db.String(50), nullable=False, primary_key=True)
#     password = db.Column(db.String(100), nullable=False)
#
#
# class Admin(db.Model):
#     __tablename__ = 'admin'
#     username = db.Column(db.String(50), nullable=False, primary_key=True)
#     password = db.Column(db.String(100), nullable=False)
