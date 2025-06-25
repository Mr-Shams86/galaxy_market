# products/mixins.py
from django.http import HttpResponseForbidden


class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.seller != request.user:
            return HttpResponseForbidden("Вы не продавец этого товара.")
        return super().dispatch(request, *args, **kwargs)
