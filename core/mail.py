# coding: utf-8
import threading

from django.core.mail import EmailMessage
from django.conf import settings


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


class SyncEmailSender(object):
    PDF_CONTENT_TYPE = 'application/pdf'
    ATTACH_FILENAME = 'order.pdf'

    def __init__(self, subject, body, recipient_list, attach=None):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.attach = attach
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def run(self):
        msg = EmailMessage(self.subject, self.body, self.from_email, self.recipient_list)
        msg.content_subtype = "html"
        if self.attach:
            msg.attach(self.ATTACH_FILENAME, self.attach, self.PDF_CONTENT_TYPE)
        msg.send()