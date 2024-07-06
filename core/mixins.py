from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class AccessRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Mixin to check if user has access to the requested resource
    """

    pass
