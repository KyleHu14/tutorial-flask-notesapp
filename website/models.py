from . import db
from flask_login import UserMixin 
from sqlalchemy.sql import func 

# All notes and users need to look like this
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    note_content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now()) # func gets the current date and time 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    # Explanation of line 10 : 
    # This is a foreign key, it stores a foreign column of another database which in this case is the id of the user who created this
    # Also called a "one to many relationship"
    # Using lower caps user since SQL references it as lower case, and .id is self explanatory

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True) # Max email length is 150, users cannot create same emails 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # A list and stores all the notes