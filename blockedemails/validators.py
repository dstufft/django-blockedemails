from itertools import ifilter
import urllib2
import logging

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.conf import settings

from blockedemails.models import Domain, Email

logger = logging.getLogger(__name__)

# Settings
BLOCK_DISPOSABLE_EMAIL_API_KEY = getattr(settings, "BLOCK_DISPOSABLE_EMAIL_API_KEY", None)
BLOCK_DISPOSABLE_EMAIL_URL = getattr(settings, "BLOCK_DISPOSABLE_EMAIL_URL",
                                     "http://check.block-disposable-email.com/api/json/%(api_key)s/%(domain)s")
BLOCK_EMAIL_ON_URLERROR = getattr(settings, "BLOCK_EMAIL_ON_URLERROR", False)

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

class DisposableEmailValidator(object):
    messages = {
        "default": _("This email address has been blocked"),
        "dea_provider": _("Temporary or disposable email addresses are not allowed"),
        "web_checked_block": _("Temporary or disposable email addresses are not allowed"),
        "domain_without_mx": _("No MX records found"),
        "fail_input_domain": _("Invalid domain name"),
        "You submitted a non existing domain": _("The domain does not exist")
    }
    code = "disposable_email"

    def __init__(self, api_key, url, block_on_fail=False):
        self.api_key = api_key
        self.url = url
        self.block_on_fail = block_on_fail

    def __call__(self, value):
        if self.api_key is None:
            return

        domain = value.rsplit("@", 1)[-1]

        try:
            resp = urllib2.urlopen(self.url % {"api_key": self.api_key, "domain": domain})
        except urllib2.URLError:
            if self.block_on_fail:
                raise ValidationError(self.messages["default"], code=self.code)
        else:
            content = json.load(resp)
            if content["request_status"] == "success":
                if content["domain_status"] == "ok":
                    return

                messages = [
                    self.messages.get(content["comment"], None),
                    self.messages.get(content["domain_status_reason"], None),
                    self.messages.get(content["domain_status"], None),
                    self.messages["default"]
                    ]
                message = ifilter(None, messages).next()
                raise ValidationError(message, code=self.code)
            elif content["request_status"] == "fail_input_domain":
                messages = [
                    self.messages.get(content["comment"], None),
                    self.messages.get(content["request_status"], None),
                    self.messages["default"]
                    ]
                message = ifilter(None, messages).next()
                raise ValidationError(message, code=self.code)
            else:
                logger.error("There was an error checking for a disposable email: Json: %s" % json.dumps(content))
                if self.block_on_fail:
                    raise ValidationError(self.messages["default"], code=self.code)


blocked_domain = DomainBlockedValidator()
blocked_email = EmailBlockedValidator()
disposable_email = DisposableEmailValidator(
    BLOCK_DISPOSABLE_EMAIL_API_KEY,
    BLOCK_DISPOSABLE_EMAIL_URL,
    block_on_fail=BLOCK_EMAIL_ON_URLERROR)