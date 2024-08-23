from django.test import SimpleTestCase
from django.urls import resolve, reverse

from jobs.views import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobSourceCreateView,
    JobSourceDeleteView,
    JobSourceDetailView,
    JobSourceListView,
    JobSourceUpdateView,
    JobUpdateView,
    TechStackCreateView,
    TechStackDeleteView,
    TechStackListView,
    TechStackUpdateView,
)


class TestJobUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        """The job list URL resolves to JobListView."""
        url = reverse("job_list")
        self.assertEqual(resolve(url).func.view_class, JobListView)

    def test_create_url_is_resolved(self):
        """The job create URL resolves to JobCreateView."""
        url = reverse("job_create")
        self.assertEqual(resolve(url).func.view_class, JobCreateView)

    def test_detail_url_is_resolved(self):
        """The job detail URL resolves to JobDetailView."""
        url = reverse("job_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobDetailView)

    def test_update_url_is_resolved(self):
        """The job update URL resolves to JobUpdateView."""
        url = reverse("job_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobUpdateView)

    def test_delete_url_is_resolved(self):
        """The job delete URL resolves to JobDeleteView."""
        url = reverse("job_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobDeleteView)


class TestJobSourceUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        """The job source list URL resolves to JobSourceListView."""
        url = reverse("job_source_list")
        self.assertEqual(resolve(url).func.view_class, JobSourceListView)

    def test_create_url_is_resolved(self):
        """The job source create URL resolves to JobSourceCreateView."""
        url = reverse("job_source_create")
        self.assertEqual(resolve(url).func.view_class, JobSourceCreateView)

    def test_detail_url_is_resolved(self):
        """The job source detail URL resolves to JobSourceDetailView."""
        url = reverse("job_source_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobSourceDetailView)

    def test_update_url_is_resolved(self):
        """The job source update URL resolves to JobSourceUpdateView."""
        url = reverse("job_source_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobSourceUpdateView)

    def test_delete_url_is_resolved(self):
        """The job source delete URL resolves to JobSourceDeleteView."""
        url = reverse("job_source_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, JobSourceDeleteView)


class TestTechStackUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        """The tech stack list URL resolves to TechStackListView."""
        url = reverse("tech_stack_list")
        self.assertEqual(resolve(url).func.view_class, TechStackListView)

    def test_create_url_is_resolved(self):
        """The tech stack create URL resolves to TechStackCreateView."""
        url = reverse("tech_stack_create")
        self.assertEqual(resolve(url).func.view_class, TechStackCreateView)

    def test_update_url_is_resolved(self):
        """The tech stack update URL resolves to TechStackUpdateView."""
        url = reverse("tech_stack_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, TechStackUpdateView)

    def test_delete_url_is_resolved(self):
        """The tech stack delete URL resolves to TechStackDeleteView."""
        url = reverse("tech_stack_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, TechStackDeleteView)
