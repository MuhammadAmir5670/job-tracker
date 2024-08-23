from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory
from jobs.models import Job, JobSource, TechStack
from jobs.tests.factories import JobFactory

User = get_user_model()


class TestJobListView(TestCase):
    base_url = reverse("job_list")
    login_url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_permission = UserFactory()
        cls.job = JobFactory(created_by=cls.user)
        view_job_permission = Permission.objects.get(codename="view_job")

        cls.user_with_permission.user_permissions.add(view_job_permission)

    def call_job_list_endpoint(self, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.get(self.base_url)

    def test_redirect_if_not_logged_in(self):
        """Non-logged-in users are redirected to the login page."""
        response = self.call_job_list_endpoint(self.user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + f"?next={self.base_url}")

    def test_forbidden_if_logged_in_but_not_authorized(self):
        """Logged-in users without the view_job permission receive a 403 error."""
        response = self.call_job_list_endpoint(self.user, authenticate=True)

        self.assertEqual(response.status_code, 403)

    def test_success_if_logged_in_user_has_view_job_permission(self):
        """Logged-in users with the view_job permission can access the job list page."""
        response = self.call_job_list_endpoint(self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/jobs_list.html")
        self.assertContains(response, self.job.title)


class TestJobDetailView(TestCase):
    login_url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_permission = UserFactory()
        cls.job = JobFactory(created_by=cls.user)
        view_job_permission = Permission.objects.get(codename="view_job")

        cls.user_with_permission.user_permissions.add(view_job_permission)

    def call_job_detail_endpoint(self, job_pk, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.get(reverse("job_detail", kwargs={"pk": job_pk}))

    def test_redirect_if_not_logged_in(self):
        """Non-logged-in users are redirected to the login page."""
        response = self.call_job_detail_endpoint(self.job.pk, self.user)
        detail_url = reverse("job_detail", kwargs={"pk": self.job.pk})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + f"?next={detail_url}")

    def test_forbidden_if_logged_in_but_not_authorized(self):
        """Logged-in users without the view_job permission receive a 403 error."""
        response = self.call_job_detail_endpoint(self.job.pk, self.user, authenticate=True)

        self.assertEqual(response.status_code, 403)

    def test_success_if_logged_in_user_has_view_job_permission(self):
        """Logged-in users with the view_job permission can access the job detail page."""
        response = self.call_job_detail_endpoint(self.job.pk, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/job_detail.html")
        self.assertContains(response, self.job.title)

    def test_404_if_job_does_not_exist(self):
        """A 404 error is returned if the requested job does not exist."""
        response = self.call_job_detail_endpoint("100", self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 404)


class TestJobCreateView(TestCase):
    base_url = reverse("job_create")
    login_url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_permission = UserFactory()
        cls.job = JobFactory(created_by=cls.user)
        cls.job_source, _ = JobSource.objects.get_or_create(name="Linkedin")
        cls.tech_stack, _ = TechStack.objects.get_or_create(name="python")
        job_permissions = Permission.objects.filter(codename__in=("view_job", "add_job"))

        cls.user_with_permission.user_permissions.set(job_permissions)

    def call_get_job_create_endpoint(self, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.get(self.base_url)

    def call_post_job_create_endpoint(self, user, payload, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.post(self.base_url, payload)

    def test_redirect_if_not_logged_in(self):
        """Non-logged-in users are redirected to the login page."""
        response = self.call_get_job_create_endpoint(self.user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + f"?next={self.base_url}")

    def test_forbidden_if_logged_in_but_not_authorized(self):
        """Logged-in users without the view_job and add_job permissions receive a 403 error."""
        response = self.call_get_job_create_endpoint(self.user, authenticate=True)

        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permissions(self):
        """Logged-in users with the view_job and add_job permissions can access the job create page."""
        response = self.call_get_job_create_endpoint(self.user_with_permission, authenticate=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/job_create.html")

    def test_form_with_empty_data(self):
        """Submitting the job form with empty data returns validation errors."""
        response = self.call_post_job_create_endpoint(self.user_with_permission, payload={}, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "This field is required.")
        self.assertFormError(response, "form", "company", "This field is required.")
        self.assertFormError(response, "form", "link", "This field is required.")
        self.assertFormError(response, "form", "job_source", "This field is required.")
        self.assertFormError(response, "form", "status", "This field is required.")
        self.assertFormError(response, "form", "tech_stacks", "This field is required.")

    def test_form_with_partial_invalid_data(self):
        """Submitting the job form with partially valid data returns validation errors."""
        data = {
            "title": "job title",
            "company": "job company name",
            "status": Job.Status.APPLIED,
            "link": "www.example.com",
        }
        response = self.call_post_job_create_endpoint(self.user_with_permission, payload=data, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "link", "Enter a valid URL.")
        self.assertFormError(response, "form", "job_source", "This field is required.")
        self.assertFormError(response, "form", "tech_stacks", "This field is required.")

    def test_form_with_valid_data(self):
        """Submitting the job form with valid data creates a new job object."""
        data = {
            "title": "job title",
            "company": "job company name",
            "status": Job.Status.APPLIED,
            "link": "https://www.example.com",
            "job_source": self.job_source.pk,
            "tech_stacks": [self.tech_stack.pk],
        }
        response = self.call_post_job_create_endpoint(self.user_with_permission, payload=data, authenticate=True)
        job = Job.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Job.objects.count(), 2)
        self.assertRedirects(response, reverse("job_detail", kwargs={"pk": job.pk}))


class TestJobUpdateView(TestCase):
    login_url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_permission = UserFactory()
        cls.job = JobFactory(created_by=cls.user)
        cls.job_source, _ = JobSource.objects.get_or_create(name="Linkedin")
        cls.tech_stack, _ = TechStack.objects.get_or_create(name="python")
        cls.base_url = reverse("job_update", kwargs={"pk": cls.job.pk})
        update_job_permission = Permission.objects.filter(codename__in=("view_job", "change_job"))

        cls.user_with_permission.user_permissions.set(update_job_permission)

    def call_get_job_update_endpoint(self, job_pk, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.get(reverse("job_update", kwargs={"pk": job_pk}))

    def call_put_job_update_endpoint(self, job_pk, payload, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.post(reverse("job_update", kwargs={"pk": job_pk}), payload)

    def test_redirect_if_not_logged_in(self):
        """Non-logged-in users are redirected to the login page."""
        response = self.call_get_job_update_endpoint(self.job.pk, self.user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + f"?next={self.base_url}")

    def test_forbidden_if_logged_in_but_not_authorized(self):
        """Logged-in users without the view_job permission receive a 403 error."""
        response = self.call_get_job_update_endpoint(self.job.pk, self.user, authenticate=True)

        self.assertEqual(response.status_code, 403)

    def test_success_if_logged_in_user_has_update_job_permission(self):
        """Logged-in users with the update_job permission can access the job update page."""
        response = self.call_get_job_update_endpoint(self.job.pk, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/job_update.html")
        self.assertContains(response, self.job.title)

    def test_404_if_job_does_not_exist(self):
        """A 404 error is returned if the requested job does not exist."""
        response = self.call_get_job_update_endpoint(100, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 404)

    def test_form_with_empty_data(self):
        """Submitting the update form with empty data returns validation errors."""
        response = self.call_put_job_update_endpoint(self.job.pk, {}, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "title", "This field is required.")
        self.assertFormError(response, "form", "company", "This field is required.")
        self.assertFormError(response, "form", "link", "This field is required.")
        self.assertFormError(response, "form", "job_source", "This field is required.")
        self.assertFormError(response, "form", "status", "This field is required.")
        self.assertFormError(response, "form", "tech_stacks", "This field is required.")

    def test_form_with_partially_valid_data(self):
        """Submitting the update form with partially valid data returns validation errors."""
        data = {
            "title": "job title",
            "job_source": self.job_source.pk,
            "status": Job.Status.APPLIED,
            "link": "www.example.com",
        }
        response = self.call_put_job_update_endpoint(self.job.pk, data, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "link", "Enter a valid URL.")
        self.assertFormError(response, "form", "company", "This field is required.")
        self.assertFormError(response, "form", "tech_stacks", "This field is required.")

    def test_form_with_valid_data(self):
        """Submitting the update form with valid data updates the job."""
        data = {
            "title": "job title (updated)",
            "company": "job company name (updated)",
            "status": Job.Status.APPLIED,
            "link": "https://www.example.com/updated",
            "job_source": self.job_source.pk,
            "tech_stacks": [self.tech_stack.pk],
        }
        response = self.call_put_job_update_endpoint(self.job.pk, data, self.user_with_permission, authenticate=True)
        self.job = Job.objects.get(pk=self.job.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("job_detail", kwargs={"pk": self.job.pk}))
        self.assertEqual(self.job.title, "job title (updated)")
        self.assertEqual(self.job.company, "job company name (updated)")
        self.assertEqual(self.job.link, "https://www.example.com/updated")


class TestJobDeleteView(TestCase):
    login_url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_permission = UserFactory()
        cls.job = JobFactory(created_by=cls.user)
        cls.url = reverse("job_delete", kwargs={"pk": cls.job.pk})
        delete_job_permission = Permission.objects.filter(codename__in=("view_job", "delete_job"))

        cls.user_with_permission.user_permissions.set(delete_job_permission)

    def call_get_job_delete_endpoint(self, job_pk, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.get(reverse("job_delete", kwargs={"pk": job_pk}))

    def call_post_job_delete_endpoint(self, job_pk, user, authenticate=False):
        if authenticate and self.user:
            self.client.force_login(user)

        return self.client.post(reverse("job_delete", kwargs={"pk": job_pk}))

    def test_redirect_if_not_logged_in(self):
        """Non-logged-in users are redirected to the login page."""
        response = self.call_get_job_delete_endpoint(self.job.pk, self.user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + f"?next={self.url}")

    def test_forbidden_if_logged_in_but_not_authorized(self):
        """Logged-in users without the delete_job permission receive a 403 error."""
        response = self.call_get_job_delete_endpoint(self.job.pk, self.user, authenticate=True)

        self.assertEqual(response.status_code, 403)

    def test_success_if_logged_in_user_has_delete_job_permission(self):
        """Logged-in users with the delete_job permission can access the job delete page."""
        response = self.call_get_job_delete_endpoint(self.job.pk, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)

    def test_success_url_and_template(self):
        """The delete view uses the correct template and returns a 200 status code."""
        response = self.call_get_job_delete_endpoint(self.job.pk, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/delete.html")

    def test_404_if_job_does_not_exist(self):
        """A 404 error is returned if the requested job does not exist."""
        response = self.call_get_job_delete_endpoint("100", self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 404)

    def test_successfully_deletes_job(self):
        """Successfully deletes the job and redirects to the job list."""
        response = self.call_post_job_delete_endpoint(self.job.pk, self.user_with_permission, authenticate=True)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("job_list"))
        self.assertEqual(Job.objects.count(), 0)
