from __future__ import unicode_literals
from django.db import models
import re, datetime
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
errors = {}


class UserManager (models.Manager):

    def basic_validator(self, postData):
        errors = {} #clear form errors so that login validation errors won't break this

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be more than 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters."

        try:
            #try to convert into datetime
            datetime.datetime.strptime(postData['bday'], "%Y-%m-%d")
        except:
            #if there is any problems converting into datetime then say it is an invalid date
            errors['bday'] = "Invalid birthday"

        # if (postData['birthday']) > datetime.date.today():
        #     errors["bday"] = "Invalid birthday"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"
        elif len(User.objects.filter(email=postData['email'])) != 0:
            errors["exist_email"] = "The email already registered."
        if len(postData['pw']) < 8:
            errors['confirm_pw'] = "pw is less than 8 characters"
        elif postData['pw'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match"

        return errors

    def login_validator(self, postData):
        errors = {} #clear form errors so that registration validation errors won't break this
        user = User.objects.get(email=postData['email'])

        print(user.pw)
        if not User.objects.filter(email=postData['email']):
            errors['invalid_email'] = "Invalid email"

        if not bcrypt.checkpw(postData['pw'].encode(),(user.pw).encode()):
            errors['invalid_pw'] = "Invalid password"

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bday = models.DateField()
    email = models.EmailField()
    pw = models.CharField(max_length=255)
    confirm_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.BooleanField(default=False)
    friends = models.ManyToManyField('self')
    # exampleonemany = models.ForeignKey(book, on_delete=models.CASCADE)
    objects = UserManager()

    def __repr__(self):
        return "<User: {} {} {}>".format(self.first_name, self.last_name, self.email, self.pw)


class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
#
#     def addFriend(self, user_id, friend_id):
#         user = self.get(id=user_id)
#         friend = self.get(id=friend_id)
#         Friend.objects.create(user_friend=user, second_friend=friend)
#         Friend.objects.create(user_friend=friend, second_friend=user)
#
#     def removeFriend(self, user_id, friend_id):
#         user = self.get(id=user_id)
#         friend = self.get(id=friend_id)
#         friendship1 = Friend.objects.get(user_friend=user, second_friend=friend)
#         friendship2 = Friend.objects.get(user_friend=friend, second_friend=user)
#         friendship1.delete()
#         friendship2.delete()
#
