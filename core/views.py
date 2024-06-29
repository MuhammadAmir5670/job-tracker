from django.views import generic


class RootView(generic.RedirectView):
    url = "/jobs"
