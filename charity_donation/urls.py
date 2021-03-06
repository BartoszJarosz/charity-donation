"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from charityapp.views import *
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_donation/', AddDonationView.as_view(), name='add_donation'),
    path('api/institutions/', InstitutionsView.as_view(), name='institutions'),
    path('user/', UserView.as_view(), name='user'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            ActivateUserView.as_view(), name='activate'),
    path('api/donations/', DonationsView.as_view(), name='donations'),
    path('api/user/donations/', UserDonationsView.as_view(), name='user_donations'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('donation/<int:id>/', DonationDetailsView.as_view(), name='donation_details'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            ResetView.as_view(), name='reset'),
]
