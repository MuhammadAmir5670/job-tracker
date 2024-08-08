from random import choice

from django.utils import timezone
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from accounts.tests.factories import UserFactory
from jobs.models import Job


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job

    title = Faker("job")
    company = Faker("company")
    link = Faker("url")
    status = LazyFunction(lambda: choice(Job.Status.values))
    applied_at = LazyFunction(lambda: timezone.now())
    created_by = SubFactory(UserFactory)
