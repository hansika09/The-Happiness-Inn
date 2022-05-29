from django import forms
from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['issue_date', 'return_date']
