from django import forms
from django.core.validators import EmailValidator

from charityapp.validators import ValidateEmail


class LoginForm(forms.Form):
    email = forms.CharField(label="email",
                            widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="password1",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class AddUserForm(forms.Form):
    name = forms.CharField(label="name", widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(label="surname", widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(label="email",
                            widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
                            validators=[EmailValidator(), ValidateEmail])
    password1 = forms.CharField(label="password1",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label="password2",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        pas1 = cleaned_data.get('password1')
        pas2 = cleaned_data.get('password2')
        if pas1 != pas2:
            raise forms.ValidationError('Hasła się różnią!')
