from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
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
        paginator_fundations = Paginator(fundations_list, 5)
        paginator_non_gov = Paginator(non_gov_list, 5)
        paginator_locals = Paginator(locals_list, 5)
        count_institution = Institution.objects.all().count()
        fundations_page = request.GET.get('fundations_page')
        non_govs_page = request.GET.get('non_govs_page')
        locals_page = request.GET.get('locals_page')
        fundations = paginator_fundations.get_page(fundations_page)
        non_govs = paginator_non_gov.get_page(non_govs_page)
        locals = paginator_locals.get_page(locals_page)
        return render(request, 'index.html', {"quantity": quantity,
                                              "count_institution": count_institution,
                                              "fundations": fundations,
                                              "non_govs": non_govs,
                                              "locals": locals})


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
        return render(request, 'donation-success.html')
