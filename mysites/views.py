from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View
from mysites.models import Site
from django.http import HttpResponseForbidden, Http404
from mysites.forms import CreateSiteForm
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator


class SiteEditMixin(View):
    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        p = request.user
        site_pk = kwargs['pk']

        try:
            s = Site.objects.get(pk=site_pk)
        except:
            raise Http404

        return super(SiteEditMixin, self).dispatch(request, *args, **kwargs) if s.profile == p \
            else HttpResponseForbidden()


class CreateSite(CreateView):
    success_url = reverse_lazy('index')
    form_class = CreateSiteForm
    template_name = 'mysites/site_form.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(CreateSite, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['profile'] = self.request.user.pk
        return initial


class UpdateSite(UpdateView, SiteEditMixin):
    model = Site
    success_url = reverse_lazy('index')
    form_class = CreateSiteForm
    template_name = 'mysites/site_update_form.html'


class DeleteSite(DeleteView, SiteEditMixin):
    model = Site
    success_url = reverse_lazy('index')
