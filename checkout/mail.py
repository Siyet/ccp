# coding: utf-8

from core.mail import EmailSender
from django.utils.safestring import mark_safe
from django.utils.text import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from wkhtmltopdf import render_pdf_from_template


class CheckoutMailer(object):
    sender_class = SyncEmailSender
    order_subject = _(u'НОВЫЙ ЗАКАЗ')
    order_customer_subject = _(u'COSTUME CODE - Ваш заказ подтвержден и оплачен')
    order_admin_template_name = 'checkout/payment_completed_admin_email.html'
    order_customer_template_name = 'checkout/payment_completed_customer_email.html'

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
    def send_to_customer_order_payment_completed(cls, order, pdf):
        subject = cls.order_customer_subject
        data = {
            'SITE_INFO_EMAIL': settings.SITE_INFO_EMAIL
        }
        html_content = mark_safe(render_to_string(cls.order_customer_template_name, data))
        cls.sender_class(subject, html_content, [order.get_customer_address().email], pdf).start()
