from django.db import models
import re
import bcrypt

class LoginManager(models.Manager):
    def user_add(self, first_name, last_name, email, bc1, bc2):
        messages = []
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email_taken = Login.loginObj.filter(email=email)

        if len(first_name) < 2:
            messages.append('First name must be at least 2 characters')
        if len(last_name) < 2:
            messages.append('Last name must be at least 2 characters')
        if not EMAIL_REGEX.match(email):
            messages.append('Not a valid email format')
        if len(email_taken) > 0:
            messages.append('Email is taken')
        if len(bc1) < 2:
            messages.append('Passwords must be at least 2 characters')
        if bc1 != bc2:
            messages.append('Passwords doesn\'t match')
        pw_hash = bcrypt.hashpw(bc1.encode(), bcrypt.gensalt()).decode()
        if len(messages) == 0:
            user =  Login.loginObj.create(first_name=first_name, last_name=last_name, email=email, bc1=pw_hash)
            return (True, user)
        else:
            return (False, messages)

    def is_logged_in(self, id):
        user = Login.loginObj.get(id=id)
        return user
        
    def login_validation(self, email, bc1):
        messages = []
        user = Login.loginObj.filter(email=email)
        if len(user) < 1:
            messages.append('Email not in database')
            return (False, messages)
        # verification
        if bcrypt.checkpw(bc1.encode(), user[0].bc1.encode()):
            user = user[0].id
            return (True, user)
        else: 
            messages.append('Incorrect password')
        return (False, messages)

class Login(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bc1 = models.CharField(max_length=255)
    bc2 = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    loginObj = LoginManager()    