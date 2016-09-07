import logging

from yandex_kassa.views import CheckOrderView as YandexCheckOrderView

from checkout.models import Order

logger = logging.getLogger('checkout')


class CheckOrderView(YandexCheckOrderView):

    def form_valid(self, form):
        response = super(CheckOrderView, self).form_valid(form)
        payment = form.get_payment()
        logger.info('Payment: %s' % payment.pk)
        order = Order.objects.get(payment=payment)
        logger.info('Order: %s' % order.pk)
        if not order.check_certificate():
            logging.error('certificate error %s' % order.pk)
            content = self.get_xml(dict(code=100, message=order.CERTIFICATE_ERROR))
            return self.get_response(content)
        logging.info('good %s' % order.pk)
        return response
