# coding: utf-8
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(subject, template, context, receivers):
    try:
        subject = u''.join(subject.splitlines())

        message = render_to_string(template, context).encode('utf-8')
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, receivers)
        msg.content_subtype = "html"
        msg.send()
        return True
    except Exception:
        # TODO: обработка ошибок
        return False
