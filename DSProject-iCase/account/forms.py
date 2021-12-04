from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import widgets

from account.models import Account


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form__input', 'placeholder': 'ระบุนามชื่อ'}
        )
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form__input', 'placeholder': 'ระบุนามสกุล'}
        )
    )

    email = forms.EmailField(
        max_length=60,
        help_text='Required. Add a valid email address',
        widget=forms.EmailInput(
            attrs={
                'class': 'form__input',
                'placeholder': 'ระบุอีเมล',
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form__input',
                'placeholder': 'ระบุรหัสผ่าน',
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form__input',
                'placeholder': "ยืนยันรหัสผ่าน",
            }
        )
    )

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'login-form-input',
            'placeholder': 'ระบุรหัสผ่าน',
        })
    )

    class Meta:
        model = Account
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'login-form-input', 'placeholder': 'ระบุอีเมล'}),
        }

    # this clean function is available to any forms that extend the ModelForm
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(
                    'Either your login email or password is incorrect.')


class AccountUpdateForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=100,required=True,widget = forms.TextInput(attrs={'class':'edit-info-form__input','placeholder':'ระบุชื่อ'}))
    # last_name= forms.CharField(max_length=100,required=True,widget = forms.TextInput(attrs={'class':'edit-info-form__input','placeholder':'ระบุนามสกุล'}))
    
    class Meta:
        model = Account
        fields = ('first_name','last_name')

    def clean_first_name(self):
        if self.is_valid():
            # assign new value
            first_name= self.cleaned_data['first_name']
            return first_name

    def clean_last_name(self):
        if self.is_valid():
            # assign new value
            last_name = self.cleaned_data['last_name']
            return last_name
