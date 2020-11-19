from django.urls import path

from .views import RouteQRCode, DashboardView, create_qr, edit_qr


urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('goto/<int:qrcode_id>', RouteQRCode.as_view(), name='goto'),
    path('makeqr', create_qr, name='create_qr'),
    path('edit_qr/<int:qrcode_id>', edit_qr, name='edit_qr')
]
