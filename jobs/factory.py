import factory
from factory.faker import faker
from faker.providers import DynamicProvider

from jobs.models import Job, TechStack

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


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    company = factory.Faker("company")
    status = factory.Faker(
        "random_element", elements=[status[0] for status in Job.Status.choices]
    )
    link = factory.Faker("url")
    applied_at = factory.Faker("date_time_this_year")

    @factory.post_generation
    def tech_stacks(self, *args, **kwargs):
        tech_stacks = [TechStackFactory() for _ in range(5)]

        self.tech_stacks.add(*tech_stacks)
