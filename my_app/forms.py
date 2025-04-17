from django import forms
from .models import Icecream

class IcecreamForm(forms.ModelForm):
    class Meta:
        model = Icecream
        fields = ['name', 'description', 'price', 'image',  'category']
