from django.urls import path

from shop.views import *

urlpatterns = [
    path('test/', test.as_view()),
    path('uploadImg/', uploadImg.as_view()),
    path('getSKUcategory/', getSKUcategory.as_view()),
    path('getSKUBrand/', getSKUBrand.as_view()),
    path('deleteCommitById/', deleteCommitById.as_view()),
]
