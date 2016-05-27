from django.db import models
from django.db.models.signals import post_save
from controller.models import SiteController
from profiles.models import MyUser

CONTENT_COICES = (
    ('head', 'Header'),
    ('body', 'Body'),
    ('a', 'Links'),
    ('p', 'Paragraphs'),
)


class Site(models.Model):
    profile = models.ForeignKey(MyUser, related_name='site', blank=False, null=False)
    url = models.URLField(blank=False, null=False, unique=True)
    # Parameters
    status = models.BooleanField(default=True, verbose_name="Status OK")
    ssl_cert = models.BooleanField(default=True, verbose_name="SSL Cert Verification")
    timeout = models.FloatField(default=0.0, verbose_name="Timeout Limit", help_text="0 Disabled.")
    address = models.BooleanField(default=True)
    ping = models.IntegerField(default=0, verbose_name="Ping Limit (ms)",
                               help_text="0 Disabled. Fails if ping > your parameter.")
    content_changed = models.BooleanField(default=False, verbose_name="Content Changed",
                                          help_text="Check if web content has been updated.")
    content_type = models.CharField(verbose_name="Type of content", help_text="Content you want to track for changes",
                                    choices=CONTENT_COICES, default=CONTENT_COICES[0], max_length=255)

    def __unicode__(self):
        return "{}".format(self.url)


def create_controller(sender, instance, **kwargs):
    try:
        SiteController.objects.get(site=instance)
    except:
        sc = SiteController(site=instance)
        sc.save()

post_save.connect(create_controller, sender=Site, dispatch_uid="create_controller")
