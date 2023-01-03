from django.contrib import admin
from .models import UserComments
from .forms import CommentForm
# Register your models here.
admin.site.register(UserComments)
# admin.site.register(CommentForm)
