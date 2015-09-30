#_*_coding:utf-8_*_
__author__ = 'jieli'

import models
from django.forms import ModelForm
from django import forms

class UserProfileForm(ModelForm):

    class Meta:
        model = models.UserProfile
        fields = ['name','department','valid_begin_time','valid_end_time']



#Test below

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32,required=True)
    name = forms.CharField(label="Real Name", max_length=32,widget=forms.TextInput(attrs={'class' : 'btn-success'}))
    email = forms.EmailField()
    passwd = forms.CharField(widget=forms.PasswordInput)