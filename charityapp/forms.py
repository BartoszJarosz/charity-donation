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


class UserSettingsForm(forms.Form):
    name = forms.CharField(label="name", widget=forms.TextInput())
    surname = forms.CharField(label="surname", widget=forms.TextInput())
    email = forms.CharField(label="email",
                            widget=forms.EmailInput(),
                            validators=[EmailValidator()])
    password = forms.CharField(label="password",
                               widget=forms.PasswordInput())

    def __init__(self, user=None, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        valid = self.user.check_password(self.cleaned_data['password'])
        if not valid:
            raise forms.ValidationError('Podaj poprawne hasło!')

    def clean_email(self):
        if self.cleaned_data['email'] != self.user.email:
            ValidateEmail(self.cleaned_data['email'])


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="password1",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    password1 = forms.CharField(label="password1",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    password2 = forms.CharField(label="password2",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        pas1 = cleaned_data.get('password1')
        pas2 = cleaned_data.get('password2')
        if pas1 != pas2:
            raise forms.ValidationError('Hasła się różnią!')

    def __init__(self, user=None, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        valid = self.user.check_password(self.cleaned_data['old_password'])
        if not valid:
            raise forms.ValidationError('Podaj poprawne hasło!')