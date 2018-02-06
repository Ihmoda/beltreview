# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import re
# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Users must submit a name"
        if len(postData['alias']) < 1:
            errors['alias'] = "Users must submit a last name"
        if len(postData['email']) < 1:
            errors['email'] = "Users must submit an email"
        if len(postData['password']) < 1:
            errors['password'] = "Users must submit a password"
        if len(postData['confirm_password']) < 1:
            errors['confirm_password'] = "Users must confirm password"

        if len(errors) > 0:
            return errors

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.-]+\@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]{2,4}$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
        PASSWORD_REGEX = re.compile(r'^.{8,}$')

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Users must submit a valid email"
        
        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name can only contain letters and must be at least two characters."
        
        if not NAME_REGEX.match(postData['alias']):
            errors['alias'] = "Last name can only contain letters and must be at least two characters."
        
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must contain at least eight characters"
        
        if not postData['password'] == postData['confirm_password']:
            errors['password'] = "Passwords must match"


        # check if email exists in the database
        result = User.objects.filter(email=postData['email'])

        if len(result) > 0:
            errors['emailexists'] = "Email already registered to user."

        return errors

    def bookvalidator(self, postData):
        errors = {}
        new_author = False
        if len(postData['book_title']) < 1:
            errors['book_title'] = "Users must submit a book title"
        else:
            result = Book.objects.filter(title=postData['book_title'])
            if len(result) > 0:
                errors['book_title'] = "Entered book already exists in database"

        if postData['select_author'] == "Select one":
            if len(postData['new_author']) < 1:
                errors['new_author'] = "Users must provide an author field."
            else:
                result = Author.objects.filter(name=postData['new_author'])
                if len(result)>0:
                    errors['new_author'] = "Specified new author already exists in database."
                else:
                    new_author = True
        else:
            #check to see if author exists
            result = Author.objects.filter(name=postData['select_author'])
            if len(result) < 1:
                errors['select_author'] = "Selected author does not exist"
        
        if len(postData['review']) < 1:
            errors['review'] = "User must provide review."
        
        try:
            rating = int(postData['rating'])
            if not rating >= 1 and not rating <= 5:
                errors['rating'] = "Rating must be an integer between 1 and 5"

        except ValueError:
            errors['rating'] = "Rating must be an integer between 1 and 5"

        return (new_author, errors)

    def authorvalidator(self, postData, bookid):
        errors = {}
        # review check
        if len(postData['review']) < 1:
            errors['review'] = "Review is required"
        
        #rating check
        try:
            rating = int(postData['rating'])
            if not rating >= 1 and not rating <= 5:
                errors['rating'] = "Rating must be an integer between 1 and 5"

        except ValueError:
            errors['rating'] = "Rating must be an integer between 1 and 5"

        
        #check to see if book exists in database

        result = Book.objects.filter(id=bookid)

        if len(result) < 1:
            errors['book'] = "Selected book does not exist in database"

        return errors
        


class User(models.Model):
    first_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add= True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add= True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add= True)
    author = models.ForeignKey(Author, related_name="books")

class Review(models.Model):
    content = models.TextField(max_length=255)
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add= True)
    user = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")









