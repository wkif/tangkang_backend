from django.urls import path

from shop.views import *

urlpatterns = [
    path('test/', test.as_view()),
]
