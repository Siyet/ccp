from django.http.response import HttpResponse
from django.template import loader
from wkhtmltopdf import render_pdf_from_template
from wkhtmltopdf.views import PDFTemplateView
from yandex_kassa.views import CheckOrderView as YandexCheckOrderView

from checkout.models import Order


class CheckOrderView(YandexCheckOrderView):

    def form_valid(self, form):
        response = super(CheckOrderView, self).form_valid(form)
        payment = form.get_payment()
        if not payment.order.check_certificate():
            content = self.get_xml(dict(code=100, message=payment.order.CERTIFICATE_ERROR))
            return self.get_response(content)
        payment.order.save_certificate()
        return response


class TestPdfView(PDFTemplateView):
    show_content_in_browser = True
    template_name = 'checkout/payment_completed_customer_email.html'

    def get(self, request, *args, **kwargs):
        t = loader.get_template(self.template_name)
        order = Order.objects.last()
        content = render_pdf_from_template(t, None, None, {'order': order})
        return HttpResponse(content, content_type='application/pdf')
