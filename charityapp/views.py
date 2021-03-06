import datetime
import smtplib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from charityapp.forms import *
from charityapp.models import *
from charityapp.tokens import account_activation_token, password_reset_token


class IndexView(View):
    def get(self, request):
        quantity = 0
        for donation in Donation.objects.all():
            quantity += donation.quantity
        count_institution = Institution.objects.all().count()
        return render(request, 'index.html', {"quantity": quantity,
                                              "count_institution": count_institution})


class RegisterView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            u = User.objects.create_user(first_name=name,
                                         last_name=surname,
                                         username=email,
                                         password=password,
                                         email=email)
            u.is_active = False
            u.save()
            message = render_to_string('acc_active_email.html', {
                'new_user': u,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                'token': account_activation_token.make_token(u),
            })
            port = 1025
            smtp_server = "localhost"
            sender_email = "my@gmail.com"
            receiver_email = u.email
            with smtplib.SMTP(smtp_server, port) as server:
                server.sendmail(sender_email, receiver_email, message)
                title = 'Rejestracja ukonczona'
                message_render = 'Rejestracja poprawnie ukonczona! Na e-mail dostaniesz link aktywacyjny!'
            return render(request, 'basic.html', {"message": message_render, "title": title})
        else:
            return render(request, 'register.html', {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return render(request, 'register.html', {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class AddDonationView(View):

    @method_decorator(login_required)
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'add-donation.html', {"categories": categories,
                                                     "institutions": institutions})

    @method_decorator(login_required)
    def post(self, request):
        quantity = request.POST['bags']
        categories = request.POST.getlist('categories')
        institution_id = int(request.POST['organization'])
        institution = Institution.objects.get(pk=institution_id)
        address = request.POST['address']
        phone_number = int(request.POST['phone'])
        city = request.POST['city']
        zip_code = request.POST['postcode']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        user = request.user
        donation = Donation.objects.create(quantity=quantity,
                                           institution=institution,
                                           address=address,
                                           phone_number=phone_number,
                                           city=city,
                                           zip_code=zip_code,
                                           pick_up_date=pick_up_date,
                                           pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment,
                                           user=user)
        for category in categories:
            donation.categories.add(Category.objects.get(name=category))
        message = 'Dziękujemy za pomoc!'
        title = 'Oddaj rzeczy'
        return render(request, 'basic.html', {"message": message, "title": title})


class UserView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user). \
            order_by('is_taken', '-pick_up_date')
        return render(request, 'user.html', {"donations": donations})


class ActivateUserView(View):

    def get(self, request, uidb64, token):
        title = 'Aktywacja konta'
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            message = 'Dziękujemy za potwierdzenie! Zostałeś zalogowany do swojego konta!'
        else:
            message = ('Link jest nieaktywny!')

        return render(request, 'basic.html', {'title': title, 'message': message})


class UserSettingsView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = UserSettingsForm(user=request.user)
        user = request.user
        form.fields['email'].widget.attrs['value'] = user.email
        form.fields['name'].widget.attrs['value'] = user.first_name
        form.fields['surname'].widget.attrs['value'] = user.last_name
        return render(request, 'user-settings.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = UserSettingsForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            if user.first_name != form.cleaned_data['name']:
                user.first_name = form.cleaned_data['name']
            if user.last_name != form.cleaned_data['surname']:
                user.last_name = form.cleaned_data['surname']
            if user.email != request.POST['email']:
                user.email = request.POST['email']
                user.username = request.POST['email']
            user.save()
            message = 'Pomyślnie zaktualizowano dane!'
            title = 'Zmiana danych'
            return render(request, 'basic.html', {'title': title, 'message': message})
        else:
            return render(request, 'user-settings.html', {'form': form})


class ChangePasswordView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'change-password.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(username=username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            message = 'Pomyślnie zmieniono hasło!'
            title = 'Zmiana hasła'
            return render(request, 'basic.html', {'title': title, 'message': message})
        else:
            return render(request, 'change-password.html', {'form': form})


class DonationDetailsView(View):

    @method_decorator(login_required)
    def get(self, request, id):
        donation = get_object_or_404(Donation, pk=id)
        return render(request, 'donation-details.html', {"donation": donation})

    @method_decorator(login_required)
    def post(self, request, id):
        donation = get_object_or_404(Donation, pk=id)
        if request.user == donation.user:
            donation.is_taken = True
            donation.taken_date = datetime.date.today()
            donation.save()
        return render(request, 'donation-details.html', {"donation": donation})


class ResetPasswordView(View):

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'reset-password.html', {"form": form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            u = User.objects.get(email=email)
            message = render_to_string('acc-reset-password-email.html', {
                'new_user': u,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                'token': password_reset_token.make_token(u),
            })
            port = 1025
            smtp_server = "localhost"
            sender_email = "my@gmail.com"
            receiver_email = u.email
            with smtplib.SMTP(smtp_server, port) as server:
                server.sendmail(sender_email, receiver_email, message)
                title = 'Zapomniane hasło'
                message_render = 'Na email wysłaliśmy link do resetowania hasła!'
            return render(request, 'basic.html', {"message": message_render, "title": title})
        else:
            return render(request, 'reset-password.html', {"form": form})


class ResetView(View):

    def get(self, request, uidb64, token):
        title = 'Resetowanie hasła'
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = ResetForm()
            return render(request, 'reset.html', {"form": form})
        else:
            message = ('Link jest nieaktywny!')
            return render(request, 'basic.html', {'title': title, 'message': message})


    def post(self, request, uidb64, token):
        title = 'Resetowanie hasła'
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = ResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()
                message = ('Pomyślnie zmieniona hasło! Możesz się teraz zalogować')
                return render(request, 'basic.html', {'title': title, 'message': message})
            else:
                return render(request, 'reset.html', {"form": form})
        else:
            message = ('Link jest nieaktywny!')
            return render(request, 'basic.html', {'title': title, 'message': message})