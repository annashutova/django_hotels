from typing import Any, Dict
from django import forms
from . import config
from datetime import date
from .models import Amenity


class DateInputWidget(forms.DateInput):
    input_type = 'date'


class RequiredInlineFormSet(forms.models.BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class HotelFilterForm(forms.Form):
    amenity_choices = ((amenity, amenity) for amenity in Amenity.objects.all())

    amenity = forms.MultipleChoiceField(choices=amenity_choices)
    star_rating = forms.MultipleChoiceField(choices=config.RATING_CHOICES)


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

    # def clean_check_in(self):
    #     check_in = self.cleaned_data.get('check_in')
    #     if check_in < date.today():
    #         raise forms.ValidationError('Check in date cannot be in the past.')
    #     return check_in

    # def clean(self) -> Dict[str, Any]:
    #     cleaned_data = super().clean()
    #     check_in = cleaned_data.get('check_in')
    #     check_out = cleaned_data.get('check_out')
    #     if check_in and check_out:
    #         if check_out <= check_in:
    #             raise forms.ValidationError('Check out date cannot be before check in date.')
