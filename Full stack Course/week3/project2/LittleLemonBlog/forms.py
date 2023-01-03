from django import forms
from .models import UserComments


class CommentForm(forms.ModelForm):

    class Meta:
        model = UserComments
        fields = '__all__'
