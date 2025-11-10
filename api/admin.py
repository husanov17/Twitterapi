from django.contrib import admin
from api.models import User, Post, Media, Comment, UserConfirmation

admin.site.register([User, Post, Media, Comment, UserConfirmation])