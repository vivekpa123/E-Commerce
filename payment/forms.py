from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):  # Changed class name to match import
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        required=True
    )
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required=True
    )
    shipping_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address1'}),
        required=True
    )
    shipping_address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address2'}),
        required=False
    )
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=True
    )
    shipping_state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=False
    )
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False
    )
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=True
    )

    class Meta:  # Proper indentation inside ShippingForm
        model = ShippingAddress
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_address1',
            'shipping_address2', 'shipping_city', 'shipping_state',
            'shipping_zipcode', 'shipping_country'
        ]
        exclude = ['user']


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on Card'}),required=True)
    card_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),required=True)
    card_exp_date = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Exp date'}),required=True)
    card_cvv_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV Code'}),required=True)
    card_address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing address1'}),required=True)
    card_address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing address2'}),required=True)
    card_city = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing city'}),required=True)
    card_state = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing state'}),required=True)
    card_zipcode =forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing zipcode'}),required=True)
    card_counrty = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing counrty'}),required=True)