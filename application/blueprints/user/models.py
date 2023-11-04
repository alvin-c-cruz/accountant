import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from application.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String())
    pass_word = db.Column(db.String())
    first_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    admin = db.Column(db.Boolean(), default=False)
    staff = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=True)
    salt = db.Column(db.String())
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def set_pass_word(self, pass_word):
        salt = os.urandom(16)
        salted_password = f"{salt}{pass_word}"
        self.salt = salt
        self.pass_word = generate_password_hash(salted_password)
        
    def check_pass_word(self, pass_word):
        salted_pass_word = f"{self.salt}{pass_word}"
        return check_password_hash(self.pass_word, salted_pass_word)
    
    def is_active(self):
        return self.active
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        if 'user_id' in session: return True
