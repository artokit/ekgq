from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('order/<uuid:uuid>/', OrderView.as_view(), name='order'),
    path('save_report/', save_report),
    path('texts/', TextReportView.as_view()),
    path('edit_text/', EditText.as_view())
]
