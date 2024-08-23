from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from jobs.models import Job, JobSource, TechStack
from jobs.tests.factories import UserFactory


class TestJobModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job_source, _ = JobSource.objects.get_or_create(name="linkedin")
        cls.user = UserFactory()
        cls.job = Job.objects.create(
            title="senior software engineer",
            company="Google",
            link="https://www.google.com",
            created_by=cls.user,
            job_source=cls.job_source,
        )

    def test_create_job(self):
        """A job can be successfully created with the given parameters."""
        job = Job.objects.create(
            title="software engineer", company="Google", created_by=self.user, job_source=self.job_source
        )

        self.assertEqual(Job.objects.count(), 2)
        self.assertEqual(job.pk, 2)
        self.assertEqual(job.title, "software engineer")
        self.assertEqual(job.company, "Google")

    def test_default_description(self):
        """The job description is an empty string by default."""
        self.assertEqual(self.job.description, "")

    def test_default_status(self):
        """The default job status is WISHLIST."""
        self.assertEqual(self.job.status, Job.Status.WISHLIST)

    def test_invalid_status(self):
        """Assigning an invalid status value raises a validation error."""
        self.job.status = "INVALID"

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_invalid_link(self):
        """Assigning an invalid link raises a validation error."""
        self.job.link = "Invalid Link"

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_job_source_cannot_be_null(self):
        """A validation error is raised if the job source is null/None."""
        self.job.job_source = None

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_created_by_cannot_be_null(self):
        """A validation error is raised if created_by is not provided or is null."""
        self.job.created_by = None

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_str(self):
        """The __str__ method returns the job title."""
        self.assertEqual(str(self.job), "senior software engineer")

    def test_get_absolute_url(self):
        """get_absolute_url returns the URL for the job detail view."""
        self.assertEqual(self.job.get_absolute_url(), reverse("job_detail", kwargs={"pk": self.job.pk}))

    def test_pretty_techstack(self):
        """pretty_techstack returns a comma-separated list of tech stack names."""
        javascript_techstack, _ = TechStack.objects.get_or_create(name="javascript")
        ruby_techstack, _ = TechStack.objects.get_or_create(name="ruby")
        go_techstack, _ = TechStack.objects.get_or_create(name="go")
        self.job.tech_stacks.add(javascript_techstack, ruby_techstack, go_techstack)

        self.assertEqual(self.job.pretty_techstack(), "go, ruby, javascript")


class TestJobSourceModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job_source = JobSource.objects.create(name="Linkedin", link_regex="[A-Z]*")

    def test_job_source_create(self):
        """
        A job source can be successfully created.
        Note: The total number of JobSource objects will include those created in tests
        plus one default object created during migration.
        """
        job_source = JobSource.objects.create(name="Glass Door", link_regex="[A-Z]*")

        self.assertEqual(JobSource.objects.count(), 3)
        self.assertEqual(job_source.name, "Glass Door")
        self.assertEqual(job_source.link_regex, "[A-Z]*")

    def test_link_regex_default_value(self):
        """The default value for link_regex is an empty string."""
        job_source = JobSource.objects.create(name="Glass Door")

        self.assertEqual(job_source.link_regex, "")

    def test_link_regex_validation(self):
        """An invalid regex for link_regex raises a validation error."""
        self.job_source.link_regex = "()()()((((("

        with self.assertRaises(ValidationError):
            self.job_source.full_clean()

    def test_str_method(self):
        """The __str__ method returns the job source name."""
        self.assertEqual(str(self.job_source), self.job_source.name)

    def test_get_absolute_url_method(self):
        """get_absolute_url returns the URL for the job source detail view."""
        self.assertEqual(
            self.job_source.get_absolute_url(),
            reverse("job_source_detail", kwargs={"pk": self.job_source.pk}),
        )
