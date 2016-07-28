from yandex_kassa.views import CheckOrderView as YandexCheckOrderView


class CheckOrderView(YandexCheckOrderView):

    def form_valid(self, form):
        response = super(CheckOrderView, self).form_valid(form)
        payment = form.get_payment()
        if not payment.order.check_certificate():
            content = self.get_xml(dict(code=100, message=payment.order.CERTIFICATE_ERROR))
            return self.get_response(content)
        payment.order.save_certificate()
        return response
