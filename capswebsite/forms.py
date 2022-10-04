from dataclasses import field
from faulthandler import disable
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'

#USER ACCOUNTS
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','numberID','college','course','year','block','password1','password2','is_student')
        widgets = {
        'is_student': forms.HiddenInput(),
     }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {'required': True, 'name': 'email', 'id': 'email', 'type': 'text', 'class': 'form-control', 'placeholder': 'Email'})
        self.fields["numberID"].widget.attrs.update(
            {'required': True, 'name': 'numberID', 'id': 'numberID', 'class': 'form-control', 'placeholder': 'Student Number'})
        self.fields["college"].widget.attrs.update(
            {'required': True, 'name': 'college', 'id': 'college', 'class': 'form-control', 'placeholder': 'College'})
        self.fields["course"].widget.attrs.update(
            {'required': True, 'name': 'course', 'id': 'course', 'class': 'form-control', 'placeholder': 'Course'})
        self.fields["year"].widget.attrs.update(
            {'required': True, 'name': 'year', 'id': 'year', 'class': 'form-control', 'placeholder': 'Year'})
        self.fields["block"].widget.attrs.update(
            {'required': True, 'name': 'block', 'id': 'block', 'class': 'form-control', 'placeholder': 'Block'})
        self.fields["password1"].widget.attrs.update(
            {'required': True, 'name': 'password1', 'id': 'password1', 'type': 'password', 'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update(
            {'required': True, 'name': 'password2', 'id': 'password2', 'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'})

        if 'college' in self.data:
            try:
                college_id = int(self.data.get('college'))
                self.fields['course'].queryset = Course.objects.filter(college=college_id).order_by('college')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.college.course_set.order_by('college')



