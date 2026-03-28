from django.urls import path

from loginAndRegister import views

urlpatterns = [
    path('signup/email', views.UserSignupEmail.as_view()),
    path('signin/email', views.SigninEmail.as_view()),
    path('signin/email/verifyOTP', views.SigninEmailVerifyOTP.as_view()),
    path('user/detail', views.UserUpdateDetail.as_view()),
    path('forget/password', views.UserForgetPassword.as_view()),
    path('forget/password/verify/otp', views.VerifyForgetPassword.as_view()),
    path('update/password', views.UpdateForgetPassword.as_view()),
    path('user/delete', views.UserDelete.as_view()),
    path('user/logout', views.UserLogOut.as_view()),
    path('retrieve/po-data', views.RetrievePurchaseOrderData.as_view()),
]
