from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Address


class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='Выбрать город').formfield(
        required=False,
    )

    class Meta:
        model = Address
        fields = ('country', 'street_address', 'zip')




