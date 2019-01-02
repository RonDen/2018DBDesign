from django import forms
from TransportationManagement.models import Car, Driver, Proposer, Accident, Record


class UserForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.PasswordInput()


class MyForm(forms.Form):
    pass


class RegisterForm(forms.Form):
    pass


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class ProposerForm(forms.ModelForm):
    class Meta:
        model = Proposer
        exclude = ['Date']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'


class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = '__all__'
