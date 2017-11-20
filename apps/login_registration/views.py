# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.contrib import messages

from .models import User, Author, Book, Review

import bcrypt


# Create your views here.
def index(request):
    return render(request, "login_registration/index.html")

def register(request):
    
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            unhashed = request.POST['password']
            hash1 = bcrypt.hashpw(unhashed.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], alias=request.POST['alias'], email=request.POST['email'], password=hash1)
            request.session['userid'] = new_user.id
            return redirect('/books')
        
    return redirect('/')


def success(request):

    if 'userid' in request.session:
        context = {
            "user": User.objects.get(id=request.session['userid']),
            "reviews": Review.objects.filter(user__id=request.session['userid']).order_by("-created_at").all()[:3],
            "other_books": Book.objects.order_by("-created_at").all()
        }

        return render(request, "login_registration/success.html", context)
    else:
        return redirect('/')


def login(request):
    
    if request.method == "POST":
        unhashedpw = request.POST['password']
        email = request.POST['email']

        login_user = User.objects.filter(email=email)
        if len(login_user) == 0:
            messages.error(request, "Incorrect username or password")
            return redirect('/')
        else:
            hashedpw = login_user[0].password
            if bcrypt.checkpw(unhashedpw.encode(), hashedpw.encode()):
                request.session['userid'] = login_user[0].id
                return redirect('/books')
            else:
                messages.error(request, "Incorrect username or password")
                return redirect('/')

    return redirect('/')

def logout(request):
    del request.session['userid']
    return redirect('/')


def newbook(request):

    if 'userid' in request.session:
        context = {
            "authors": Author.objects.all()
        }
        return render(request, "login_registration/newreview.html", context)
    else:
        return redirect('/')


def add(request):

    if request.method == "POST" and 'userid' in request.session:
        validation_data = User.objects.bookvalidator(request.POST)
        errors = validation_data[1]
        new_author = validation_data[0]
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/new')
        else:
            if new_author:
                author = Author.objects.create(name=request.POST['new_author'])
            else:
                author = Author.objects.get(name=request.POST['select_author'])
            
            user = User.objects.get(id=request.session['userid'])
            book = Book.objects.create(title=request.POST['book_title'], author=author)
            Review.objects.create(content=request.POST['review'], book=book, user=user, stars=request.POST['rating'])
            return redirect('/books/new')

    return redirect('/')

def book(request, bookid):

    if 'userid' in request.session:
        context = {
            "book": Book.objects.get(id=bookid),
            "reviews": Review.objects.filter(book__id=bookid).order_by("-created_at"),
        }

        return render(request, "login_registration/book.html", context)

    return redirect('/books')

def addreview(request, bookid):
    
    if request.method == "POST" and 'userid' in request.session:
        errors = User.objects.authorvalidator(request.POST, bookid)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/' + str(bookid))
        else:
            user = User.objects.get(id=request.session['userid'])
            book= Book.objects.get(id=bookid)
            Review.objects.create(content=request.POST['review'], stars=request.POST['rating'], user=user, book=book)
            return redirect('/books/' + str(bookid))

    return redirect('/books/' + str(bookid))


def deletereview(request, bookid, reviewid):
    print "hit deletereview"
    if 'userid' in request.session:
        print "hit initial check"
        # get the userid from the selected review
        review_result = User.objects.filter(reviews__id=reviewid)
        if len(review_result) > 0:
            print "passed len check"
            if review_result[0].id == request.session['userid']:
                Review.objects.get(id=reviewid).delete()
                return redirect('/books/' + str(bookid))

    return redirect('/books/' + str(bookid))


def user(request, userid):
    if 'userid' in request.session:
        #check if userid exists
        result = User.objects.filter(id=userid)
        
        if len(result) > 0:
            
            context = {
                "user": result[0],
                "books_reviewed": Book.objects.filter(reviews__user__id=request.session['userid']),
                "review_count": Review.objects.filter(user__id=userid).count()
            }

            return render(request, "login_registration/users.html", context)

    return redirect('/')


