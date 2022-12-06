from django.forms import ModelForm
from .models import Drinks


class DrinkAdd(ModelForm):
    class Meta:
        model = Drinks
        fields = '__all__'
    