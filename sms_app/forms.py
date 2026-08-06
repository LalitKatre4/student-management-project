from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = Student
        fields = [

            'name',
            'email',
            'contact',
            'course',
            'address',
            'photo',
            'age',
            'gender',
            'password'
        ]

class StudentProfileForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            'contact',
            'address',
            'photo'
        ]