from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from charityapp.models import Institution, Category
from api.serializers import *


class InstitutionsView(APIView):
    def get(self, request):
        page = request.GET.get('page')
        organizations_type = request.GET.get('type')
        if page and organizations_type:
            organizations_list = Institution.objects.filter(type=organizations_type).order_by('name')
            paginator = Paginator(organizations_list, 5)
            if int(page) > paginator.num_pages:
                raise Http404
            organizations = paginator.get_page(page)
        else:
            organizations = Institution.objects.all()
        serializer = InstitutionSerializer(organizations, many=True, context={"request": request})
        return Response(serializer.data)


class DonationsView(APIView):
    def get(self, request):
        donations = Donation.objects.all()
        serializer = DonationSerializer(donations, many=True, context={"request": request})
        return Response(serializer.data)

class UserDonationsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404
        donations = Donation.objects.filter(user=request.user)
        serializer = DonationSerializer(donations, many=True, context={"request": request})
        return Response(serializer.data)









# # filter by categories
# categories = request.GET.getlist('categories')
# if categories:
#     cat_list = []
#     for category in categories:
#         try:
#             cat_list.append(Category.objects.get(name=category))
#         except Category.DoesNotExist:
#             raise Http404
#     try:
#         institutions = Institution.objects.filter(categories__in=cat_list).distinct()
#     except Institution.DoesNotExist:
#         raise Http404
#     serializer = InstitutionSerializer(institutions, many=True, context={"request": request})
# else:
#     institutions = Institution.objects.all()
#     serializer = InstitutionSerializer(institutions, many=True, context={"request": request})
