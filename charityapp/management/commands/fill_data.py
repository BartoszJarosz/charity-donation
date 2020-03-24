from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random

from faker import Faker

from charityapp.models import *

CATEGORY_NAMES = ['zabawki', 'elektronika', 'ubrania', 'jedzenie', 'meble']


class Command(BaseCommand):
    help = 'Wypełnianie podstawowych danych'

    def handle(self, *args, **options):
        fake = Faker('pl_PL')
        for _ in range(50):
            email = fake.email()
            u = User.objects.filter(email=email)
            if not u:
                User.objects.create_user(first_name=fake.first_name(),
                                         last_name=fake.last_name(),
                                         password='password',
                                         username=email,
                                         email=email)
        for category in CATEGORY_NAMES:
            Category.objects.create(name=category)

        for _ in range(50):
            i = Institution.objects.create(name=fake.company(),
                                           description=fake.text(),
                                           type=random.randint(1, 3))
            categories = random.sample(list(Category.objects.all()), random.randint(1, 5))
            for category in categories:
                i.categories.add(category)

        instytutions = Institution.objects.all()
        users = User.objects.all()
        for _ in range(100):
            instytution = random.choice(instytutions)
            user = random.choice(users)
            donation = Donation.objects.create(quantity=random.randint(1, 10),
                                               institution=instytution,
                                               address=fake.street_address(),
                                               phone_number=random.randint(100000000, 999999999),
                                               city=fake.city(),
                                               zip_code=fake.postcode(),
                                               pick_up_date=fake.future_date(),
                                               pick_up_time=fake.time(),
                                               pick_up_comment=fake.text(),
                                               user=user)
            categories = random.sample(list(Category.objects.all()), random.randint(1, 5))
            for category in categories:
                donation.categories.add(category)
