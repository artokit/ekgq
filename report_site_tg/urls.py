from django.urls import path
from .views import Index, OrderView, save_report

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('order/<uuid:uuid>/', OrderView.as_view(), name='order'),
    path('save_report/', save_report)
]
