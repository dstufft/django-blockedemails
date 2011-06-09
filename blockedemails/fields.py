from django import forms

from blockedemails.validators import blocked_domain, blocked_email, disposable_email

class EmailField(forms.EmailField):
    default_validators = forms.EmailField.default_validators + [blocked_domain, blocked_email, disposable_email]