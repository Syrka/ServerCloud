from django.db import models


class SiteController(models.Model):
    site = models.OneToOneField("mysites.Site", related_name='site_controller', null=False, blank=False)
    status = models.CharField(max_length=255, default='', null=True, blank=True)
    ssl = models.BooleanField(blank=True, default=True)
    timeout = models.CharField(null=True, blank=True, max_length=20)
    address = models.CharField(blank=True, default="0.0.0.0", max_length=255)
    ping = models.FloatField(null=True, blank=True)
    changed = models.BooleanField(blank=True, default=False)
    content = models.CharField(blank=True, max_length=200, default='xx')
    last_updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __unicode__(self):
        return "{} Controller".format(self.site)
