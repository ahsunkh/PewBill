from django.urls import path

from adminFunctions import views

urlpatterns = [
    path('user/management', views.UserManagement.as_view()),

    path('get/company', views.CompanyGet.as_view()),
    path('company/detail/<pk>', views.CompanyDetail.as_view()),
    path('retrieve/companies/counts', views.TotalNumberCompanies.as_view()),

    path('get/category', views.CategoryGet.as_view()),
    path('category/detail/<pk>', views.CategoryDetail.as_view()),

    path('get/product', views.ProductGet.as_view()),
    path('product/detail/<pk>', views.ProductDetail.as_view()),

    path('get/purchaseorder', views.PurchaseOrderManagement.as_view()),
    path('purchaseorder/detail/<pk>', views.PurchaseOrderDetail.as_view()),

    path('retrieve/p_o', views.PewStats.as_view()),

    path('get/order-detail', views.OrderDetailManagement.as_view()),
    path('order-detail/<pk>', views.OrderDetailDetail.as_view()),

    path('retrieve/order_detail/<pk>', views.GetPurchaseOrderByON.as_view()),

    path('retrieve/challan/date', views.ChallanStats.as_view()),

    path('get/challan', views.ChallanManagement.as_view()),

    path('challan/detail/<pk>', views.ChallanDetail.as_view()),
    path('challan/sendbyemail/<pk>', views.ChallanSendByEmail.as_view()),
    path('challan/download/<pk>', views.ChallanPDF.as_view()),


    path('challan/company/<pk>', views.ChallanByCompany.as_view()),


    path('get/delivery', views.DeliveryRecordGet.as_view()),

    path('get/bill', views.BillManagement.as_view()),
    path('bill/detail/<pk>', views.BillDetail.as_view()),
    path('bill/download/<pk>', views.BillDownloadPDF.as_view()),
    path('bill/sendbyemail/<pk>', views.BillSendByEmail.as_view()),
    path('retrieve/bill/date', views.BillStats.as_view()),


    path('check/quantity', views.OrderDetailCheckQuantity.as_view()),


    path('employee/contact', views.ContactManagement.as_view()),





]
