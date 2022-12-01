from django.urls import path

from adminFunctions import views

urlpatterns = [
    path('user/management', views.UserManagement.as_view()),

    path('get/company', views.CompanyGet.as_view()),
    path('company/detail/<pk>', views.CompanyDetail.as_view()),

    path('get/category', views.CategoryGet.as_view()),
    path('category/detail/<pk>', views.CategoryDetail.as_view()),

    path('get/product', views.ProductGet.as_view()),
    path('product/detail/<pk>', views.ProductDetail.as_view()),

    path('get/purchaseorder', views.PurchaseOrderGet.as_view()),
    path('purchaseorder/detail/<pk>', views.PurchaseOrderDetail.as_view()),

    path('retrieve/p_o', views.PewStats.as_view()),

    path('get/orderdetail', views.OderDetailGet.as_view()),
    path('oderdetail/detail/<pk>', views.OrderDetailDetail.as_view()),

    path('retrieve/order_detail/<pk>', views.GetPurchaseOrderByON.as_view()),

    path('get/challan', views.ChallanGet.as_view()),
    path('challan/detail/<pk>', views.ChallanDetail.as_view()),

    # path('get/challan', views.DeliveryRecord.as_view()),

    path('get/bill', views.BillGet.as_view()),
    path('bill/detail/<pk>', views.BillDetail.as_view()),










]
