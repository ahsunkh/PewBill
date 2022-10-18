from django.urls import path

from adminFunctions import views

urlpatterns = [
    path('get/company', views.CompanyGet.as_view()),
    path('company/detail/<pk>', views.CompanyDetail.as_view()),

    path('get/category', views.CategoryGet.as_view()),
    path('category/detail/<pk>', views.CategoryDetail.as_view()),

    path('get/product', views.ProductGet.as_view()),
    path('product/detail/<pk>', views.ProductDetail.as_view()),
]
