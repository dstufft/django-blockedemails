from django.utils.translation import ugettext_lazy as _
from django.db import models

class Domain(models.Model):
    domain = models.CharField(max_length=300, unique=True)

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")

    def __unicode__(self):
        return u"%s" % (self.domain,)

class Email(models.Model):
    email = models.EmailField(max_length=300, unique=True)

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")

    def __unicode__(self):
        return u"%s" % (self.email,)