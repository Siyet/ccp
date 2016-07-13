# coding: utf-8
import threading

from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings


class EmailSender(threading.Thread):
    def __init__(self, subject, body, recipient_list):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = settings.DEFAULT_FROM_EMAIL
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.body, self.from_email, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


class CostumecodeMailer(object):
    sender_class = EmailSender

    @classmethod
    def send_order_payment_completed(cls, order):
        data = {
            'order': order, 
            'SITE_DOMAIN': settings.SITE_DOMAIN
        }
        subject = _(u'НОВЫЙ ЗАКАЗ')
        html_content = mark_safe(render_to_string('checkout/payment_completed_admin_email.html', data))
        cls.sender_class(subject, html_content, [settings.ADMIN_ORDER_EMAIL]).start()
