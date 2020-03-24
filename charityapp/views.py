from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from charityapp.forms import *
from charityapp.models import *


class IndexView(View):
    def get(self, request):
        quantity = 0
        for donation in Donation.objects.all():
            quantity += donation.quantity
        fundations_list = Institution.objects.filter(type=1)
        non_gov_list = Institution.objects.filter(type=2)
        locals_list = Institution.objects.filter(type=3)
        paginator = Paginator(fundations_list, 5)
        count_institution = Institution.objects.all().count()
        page = request.GET.get('page')
        fundations = paginator.get_page(page)
        return render(request, 'index.html', {"quantity": quantity,
                                              "count_institution": count_institution,
                                              "fundations": fundations})


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
            User.objects.create_user(first_name=name,
                                     last_name=surname,
                                     username=email,
                                     password=password,
                                     email=email)
            return render(request, 'register-complete.html')
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
    def get(self, request):
        return render(request, 'add-donation.html')
