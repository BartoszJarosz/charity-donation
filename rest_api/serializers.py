from rest_framework import serializers

from charityapp.models import Institution, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class InstitutionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Institution
        fields = ("name", 'description', 'categories')
