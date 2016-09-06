from yandex_kassa.views import CheckOrderView as YandexCheckOrderView

from checkout.models import Order


class CheckOrderView(YandexCheckOrderView):

    def form_valid(self, form):
        response = super(CheckOrderView, self).form_valid(form)
        payment = form.get_payment()
        order = Order.objects.get(payment=payment)
        if not order.check_certificate():
            content = self.get_xml(dict(code=100, message=order.CERTIFICATE_ERROR))
            return self.get_response(content)
        order.save_certificate()
        return response
