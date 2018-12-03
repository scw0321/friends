from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime


def index(request):
    return render(request, 'index.html')


# this function is called when the login button in index.html is pressed
def login(request):
    print("LOGING")

    errors = User.objects.login_validator(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        #get the current user from the database
        currentuser = User.objects.get(email=request.POST['email'])

        #set the session
        request.session['id'] = currentuser.id
        request.session['first_name'] = currentuser.first_name
        return redirect('/show')

# this function is called when the register button in index.html is pressed
def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:

        encoded_pw_in = request.POST['pw'].encode()
        pw_hash = bcrypt.hashpw(encoded_pw_in, bcrypt.gensalt())

        new_guy = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            bday=request.POST['bday'],
            email=request.POST['email'],
            pw = pw_hash.decode()
        )
        new_guy.save()
        # messages.success(request, "Success!")

        #set the session
        request.session['id'] = new_guy.id
        request.session['first_name'] = new_guy.first_name

        # redirect to show which calls show function to render the friends page
        return redirect('/show')

def logout(request):
    if request.method == "GET":
        request.session.clear()
        return redirect('/')

#this function renders the profile.html page.
def profile(request, number):
    if request.method == "GET":
        query = User.objects.get(id=number)
        comments = Comment.objects.filter(poster = query)
    return render(request, "profile.html", {"user": query, 'comments': comments})

# def show(request, number):
#     print("hi2")
#     if request.method == "GET":
#         query = User.objects.get(id=number)
#     return render(request, "show.html", {"user": query})

#this is called when adding a friend in the friends.html
def friend(request, number):
    print(request.session['id'])
    if request.method == "GET":
        myid = request.session['id']

        #get my object from the database
        me = User.objects.get(id=myid)

        #get target friends object from the database
        friend = User.objects.get(id=number)

        #add target friend to my friends list
        me.friends.add(friend)
        me.save()

    #redirect to show to render the page
    return redirect('/show')

#this is called when adding a friend in the friends.html
def unfriend(request, number):
    print(request.session['id'])
    if request.method == "GET":
        myid = request.session['id']
        me = User.objects.get(id=myid)
        friend = User.objects.get(id=number)
        me.friends.remove(friend)

        me.save()

    return redirect('/show')


#this function renders the friends.html page. Only available after login
def show(request):
    if request.method == "GET":
        # query = User.objects.get(id=number)

        myid = request.session['id']
        friends = User.objects.filter(friends__id=myid)
        nonfriends = User.objects.all().exclude(id=myid).exclude(friends__id=myid)

        context = {
            'friends': friends,
            'nonfriends': nonfriends
            }

        return render(request, 'friends.html', context)

#this function is called when post comment in the profile.html page
def post(request, number):
    print(request.POST)
    user = User.objects.get(id=number)

    new_comment = Comment.objects.create(
        comment=request.POST['post'],
        poster=user
    )
    new_comment.save()
    return redirect('/'+number)

#this function is called when delete comment in the profile.html page
#don't let you delete if the comment is older than MAX_COMMENT_TIME_SECONDS

def delete_comment(request, number, comment_id):

    MAX_COMMENT_TIME_SECONDS = 10
    comment = Comment.objects.get(id=comment_id)

    # get the current time in utc. (datetime in database is in utc form
    now = datetime.datetime.utcnow()

    # get rid of the timezone info (not sure if needed)
    created_at = comment.created_at.replace(tzinfo=None)

    # find the difference between current time and created time
    diff = now-created_at

    # if difference is greater than 10 seconds don't allow comment to be deleted (add appropriate error message)
    if diff.seconds <= MAX_COMMENT_TIME_SECONDS:
        comment.delete()

    # redirect back to profile url that will call profile function
    return redirect('/'+number)

# def profile(request, id):
#     profile = User.objects.get(id=id)
#     context = {
#         'user': profile
#     }
#     return render(request, 'profile.html', context)
# Create your views here.
