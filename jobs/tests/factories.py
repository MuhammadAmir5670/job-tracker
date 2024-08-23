from random import choice

import factory
from django.utils import timezone
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker.providers import DynamicProvider

from accounts.tests.factories import UserFactory
from jobs.models import Job, JobSource, TechStack

tech_stack_provider = DynamicProvider(
    provider_name="tech_stack",
    elements=[
        "LAMP",
        "MEAN",
        "MERN",
        "JAMstack",
        ".NET",
        "Ruby on Rails",
        "Django",
        "Spring",
        "Flutter",
        "React Native",
        "Vue.js",
        "Serverless",
        "ELK",
        "ELT",
        "Hadoop",
        "Kubernetes",
        "TensorFlow",
        "PyTorch",
        "Blockchain",
        "GraphQL",
        "Redis",
    ],
)
factory.Faker.add_provider(tech_stack_provider)


class TechStackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TechStack
        django_get_or_create = ("name",)

    name = factory.Faker("tech_stack")


class JobSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobSource
        django_get_or_create = ("name",)

    name = factory.Faker("name")


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job

    title = Faker("job")
    company = Faker("company")
    link = Faker("url")
    status = LazyFunction(lambda: choice(Job.Status.values))
    applied_at = LazyFunction(lambda: timezone.now())
    job_source = SubFactory(JobSourceFactory)
    created_by = SubFactory(UserFactory)
