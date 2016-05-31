from django.http import HttpResponse
from mysites.models import Site
from controller.models import SiteController
from django.views.generic import DetailView
import requests
import socket
import hashlib
from BeautifulSoup import BeautifulSoup, SoupStrainer

from ServerCloud.settings import EMAIL_HOST_USER
from google.appengine.api import mail


class ControllerDetailView(DetailView):
    model = SiteController
    template_name = 'controller/controller_detail.html'

    def dispatch(self, request, *args, **kwargs):
        update_all(self.request)
        return super(ControllerDetailView, self).dispatch(request, *args, **kwargs)


def update_status(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.status:
            try:
                status = requests.get(site.url).status_code
            except:
                return HttpResponse()  # Could raise SSL Certificate Error
            controller.status = status
            controller.save()
            if status != 200:
                mail.send_mail(sender=EMAIL_HOST_USER,
                               to=[site.profile.email],
                               subject="Status Error",
                               body="Your site {} is not OK. Its status is {}.".format(site.url, controller.status)
                               )
    return HttpResponse()


def update_address(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.address:
            url = site.url.split('://')
            url = url[-1].replace('/', '')
            try:
                address = socket.gethostbyname(url)
            except:
                address = "0.0.0.0"

            # if not address has been settled yet
            if controller.address == "0.0.0.0":
                controller.address = address

            if controller.address != address and controller.address != "0.0.0.0":
                mail.send_mail(sender=EMAIL_HOST_USER,
                               to=[site.profile.email],
                               subject="Host Address",
                               body= "The host address of the site {} "
                                     "has changed. Check if it's a valid address."
                                     " The new address is {}".format(site.url, controller.address),
                               )

            controller.address = address
            controller.save()
    return HttpResponse()


def update_timeout(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.timeout != 0.0:
            try:
                requests.get(site.url, timeout=site.timeout)
            except requests.exceptions.ConnectTimeout:
                controller.timeout = "Failed"
                controller.save()
                mail.send_mail(sender=EMAIL_HOST_USER,
                               to=[site.profile.email],
                               subject="Timeout.",
                               body="Your site {} is loading too slow, "
                               )

            except requests.exceptions.ConnectionError:
                controller.timeout = "Failed"
                controller.save()

                mail.send_mail(sender=EMAIL_HOST_USER,
                               to=[site.profile.email],
                               subject="Site down.",
                               body="Your site {} is out, "
                                    " check if the url is correct.".format(site.url, site.timeout)
                               )
            except requests.exceptions.ChunkedEncodingError:
                controller.timeout = "Failed"
                controller.save()

            else:
                controller.timeout = "OK"
                controller.save()
    return HttpResponse()


def update_ssl(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.ssl_cert:
            try:
                r = requests.get(site.url, verify=True)
                if r.ok is False:
                    raise requests.exceptions.SSLError
            except requests.exceptions.SSLError:
                controller.ssl = False
                controller.save()

                mail.send_mail(sender=EMAIL_HOST_USER,
                               to=[site.profile.email],
                               subject="SSL Error",
                               body="No SSL Certificate in site {}".format(site.url)
                               )
            else:
                controller.ssl = True
                controller.save()
    return HttpResponse()


def update_ping(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.ping:
            try:
                r = requests.get(site.url)
                ping = r.elapsed.total_seconds()
                controller.ping = ping * 1000
                controller.save()
                if ping * 1000 > site.ping:

                    mail.send_mail(sender=EMAIL_HOST_USER,
                                   to=[site.profile.email],
                                   subject="Ping problems.",
                                   body="Your site {} loaded in {} miliseconds."
                                        " More than the {} miliseconds you specified.".format(site.url, ping * 1000, site.ping)
                                   )
            except requests.exceptions.ChunkedEncodingError:
                pass
    return HttpResponse()


def update_content_changed(request):
    for site in Site.objects.all():
        controller = site.site_controller

        if site.content_changed:
            try:
                r = requests.get(site.url).content
                soup = BeautifulSoup(r, parseOnlyThese=SoupStrainer(site.content_type))
                content = hashlib.md5(soup.text.encode('utf-8')).hexdigest()

                if controller.content != content and controller.content != "xx":
                    controller.changed = True
                    controller.save()

                    mail.send_mail(sender=EMAIL_HOST_USER,
                                   to=[site.profile.email],
                                   subject="Content change.",
                                   body="The content of your site {} has been modified.".format(site.url)
                                   )

                if controller.content == content:
                    controller.changed = False

                controller.content = content
                controller.save()

            except requests.exceptions.ChunkedEncodingError:
                controller.changed = False
                controller.save()

    return HttpResponse()


def update_all(request):
    update_status(request)
    update_address(request)
    update_timeout(request)
    # update_ssl(request)
    update_ping(request)
    update_content_changed(request)
