from django import forms
from . import config


class DateInputWidget(forms.DateInput):
    input_type = 'date'


class RequiredInlineFormSet(forms.models.BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class HotelFindForm(forms.Form):
    country = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter a country'}),
        max_length=config.CHARS_DEFAULT,
        required=True
        )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter a city'}),
        max_length=config.CHARS_DEFAULT,
        required=True
        )
    check_in = forms.DateField(widget=DateInputWidget, required=True)
    check_out = forms.DateField(widget=DateInputWidget, required=True)
    capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a number of people'}),
        min_value=1,
        required=True
        )


class PersonalData(forms.Form):
    first_name = forms.CharField(max_length=config.CHARS_DEFAULT)
    last_name = forms.CharField(max_length=config.CHARS_DEFAULT)
    phone = forms.CharField(max_length=config.PHONE_LENGTH)
    date_of_birth = forms.DateField(widget=DateInputWidget)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=config.CHARS_DEFAULT)
    email = forms.CharField(max_length=config.CHARS_DEFAULT)
    first_name = forms.CharField(max_length=config.CHARS_DEFAULT)
    last_name = forms.CharField(max_length=config.CHARS_DEFAULT)
    phone = forms.CharField(max_length=config.PHONE_LENGTH)
    date_of_birth = forms.DateField(widget=DateInputWidget)
    password1 = forms.CharField(max_length=config.CHARS_DEFAULT, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=config.CHARS_DEFAULT, widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(max_length=config.CHARS_DEFAULT)
    password = forms.CharField(max_length=config.CHARS_DEFAULT, widget=forms.PasswordInput())
