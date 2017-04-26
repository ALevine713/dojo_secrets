from __future__ import unicode_literals

from django.db import models
import re, datetime, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        if len(data['fnom']) < 2:
            errors.append("First name must be at least 2 characters long.")
        if not data['fnom'].isalpha():
            errors.append("First name may only be letters")
        if len(data['lnom']) < 2:
            errors.append("Last name must be at least 2 characters long.")
        if not data['lnom'].isalpha():
            errors.append("Last name may only be letters")
        if data['e_address'] == '':
            errors.append("Email may not be blank")
        if not EMAIL_REGEX.match(data['e_address']):
            errors.append("Please enter a vailid email address")
        try:
            User.objects.get(email = data['e_address'])
            errors.append("Email is already registered, please log in.")
        except:
            pass
        if len(data['pass_word']) < 8:
            errors.append("Password must be at least 8 characters long.")
        if data['pass_word'] != data['confirm_pass_word']:
            errors.append("Password and confirm password does not match.")
        if len(errors) == 0:
            print('no errors')
            data['pass_word'] = bcrypt.hashpw(data['pass_word'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(first_name=data['fnom'], last_name=data['lnom'], email=data['e_address'], password=data['pass_word'])
            return {
                'new': new_user,
                'error_list': None,
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }
    def log(self, log_data):
        errors = []
        try:
            found_user = User.objects.get(email=log_data['e_mail'])
            if bcrypt.hashpw(log_data['p_word'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect Password.")
        except:
            errors.append("Email Address is not registered")
        if len(errors) == 0:
            return {
                'logged_user': found_user,
                'list_errors': None,
            }
        else:
            return {
                'logged_user': None,
                'list_errors': errors,
            }

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Secret(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='secrets_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='user_likes')
    secret = models.ForeignKey(Secret, related_name='secret_likes')
