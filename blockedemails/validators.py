from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from blockedemails.models import Domain, Email

class BaseBlockedValidator(object):
    message = _("This email address has been blocked")
    code = "blocked"

class DomainBlockedValidator(BaseBlockedValidator):
    message = _("This domain has been blocked")
    code = "blocked_domain"

    def __call__(self, value):
        try:
            Domain.objects.get(domain=value.rsplit("@", 1)[-1])
        except Domain.DoesNotExist:
            pass
        else:
            raise ValidationError(self.message, self.code)

class EmailBlockedValidator(BaseBlockedValidator):
    code = "blocked_email"

    def __call__(self, value):
        try:
            Email.objects.get(email=value.split("+", 1)[0])
        except Email.DoesNotExist:
            pass
        else:
            raise ValidationError(self.message, self.code)

blocked_domain = DomainBlockedValidator()
blocked_email = EmailBlockedValidator()