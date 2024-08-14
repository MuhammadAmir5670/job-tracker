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
        """Job is created with the given parameters"""
        job = Job.objects.create(
            title="software engineer", company="Google", created_by=self.user, job_source=self.job_source
        )

        self.assertEqual(Job.objects.count(), 2)
        self.assertEqual(job.pk, 2)
        self.assertEqual(job.title, "software engineer")
        self.assertEqual(job.company, "Google")

    def test_default_status(self):
        """Job status default value is WISHLIST"""
        self.assertEqual(self.job.status, Job.Status.WISHLIST)

    def test_invalid_status(self):
        """Job status value apart from Job.Status choices raises validation Error"""
        self.job.status = "INVALID"

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_invalid_link(self):
        """Invalid job link raises validation error"""
        self.job.link = "Invalid Link"

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_job_source_cannot_be_null(self):
        """Raises validation error if job_source is null/None"""
        self.job.job_source = None

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_created_by_cannot_be_null(self):
        """Job created_by raises db constraint error if not provided or given null"""
        self.job.created_by = None

        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_str(self):
        self.assertEqual(str(self.job), "senior software engineer")

    def test_get_absolute_url(self):
        """job get_absolute_url returns the job detail url"""
        self.assertEqual(self.job.get_absolute_url(), reverse("job_detail", kwargs={"pk": self.job.pk}))

    def test_pretty_techstack(self):
        javascript_techstack, _ = TechStack.objects.get_or_create(name="javascript")
        ruby_techstack, _ = TechStack.objects.get_or_create(name="ruby")
        go_techstack, _ = TechStack.objects.get_or_create(name="go")
        self.job.tech_stacks.add(javascript_techstack, ruby_techstack, go_techstack)

        self.assertEqual(self.job.pretty_techstack(), "go, ruby, javascript")
