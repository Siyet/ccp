# coding: utf-8
import threading

from django.core.mail import EmailMessage
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from wkhtmltopdf import render_pdf_from_template


class EmailSender(threading.Thread):
    PDF_CONTENT_TYPE = 'application/pdf'
    ATTACH_FILENAME = 'order.pdf'

    def __init__(self, subject, body, recipient_list, attach=None):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.attach = attach
        self.from_email = settings.DEFAULT_FROM_EMAIL
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.body, self.from_email, self.recipient_list)
        msg.content_subtype = "html"
        if self.attach:
            msg.attach(self.ATTACH_FILENAME, self.attach, self.PDF_CONTENT_TYPE)
        msg.send()


class CostumecodeMailer(object):
    sender_class = EmailSender
    order_subject = _(u'НОВЫЙ ЗАКАЗ')
    order_admin_template_name = 'checkout/payment_completed_admin_email.html'
    order_pdf_template_name = 'checkout/payment_completed_customer_email.html'

    @classmethod
    def send_order_payment_completed(cls, order):
        data = {
            'order': order, 
            'SITE_DOMAIN': settings.SITE_DOMAIN
        }
        subject = cls.order_subject
        html_content = mark_safe(render_to_string(cls.order_admin_template_name, data))
        cls.sender_class(subject, html_content, [settings.ADMIN_ORDER_EMAIL]).start()

    @classmethod
    def send_to_customer_order_payment_completed(cls, order):
        t = loader.get_template(cls.order_pdf_template_name)
        pdf = render_pdf_from_template(t, None, None, {'order': order})
        subject = cls.order_subject
        cls.sender_class(subject, '', [order.get_customer_address().email], pdf).start()
