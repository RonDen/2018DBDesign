from django import forms
from TransportationManagement.models import Car, Driver, Proposer


class UserForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.PasswordInput()


class MyForm(forms.Form):
    pass


class RegisterForm(forms.Form):
    pass


class DriverForm(forms.Form):
    pass


class CarForm(forms.Form):
    class Meta:
        car = Car
        fields = ['CNo', 'CType', 'COiConsumpution']


class ProposerForm(forms.Form):
    pass
