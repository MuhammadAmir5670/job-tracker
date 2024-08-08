from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = LazyAttribute(lambda user: f"{user.username}@gmail.com")
    password = "123456"
