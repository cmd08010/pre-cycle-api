from django.urls import path
from .views.scan_views import Scans, ScanDetail, ScanApiDetail
from .views.item_views import Items, ItemDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword, Admin, AdminDetail

urlpatterns = [
  	# Restful routing
    path('add-item/', Items.as_view(), name='scans'),
    path('get-items/', Items.as_view(), name='scans'),
    path('scans/', Scans.as_view(), name='scans'),
    path('get-item/', ItemDetail.as_view(), name='items'),
    path('scans/<int:pk>/', ScanDetail.as_view(), name='scan_detail'),
    path('scan-item/<str:slug>/', ItemDetail.as_view(), name='scan_detail'),
    path('scan-item/<str:slug>/api/', ScanApiDetail.as_view(), name='scan_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('users/<int:pk>/', AdminDetail.as_view(), name='admin'),
    path('users/', Admin.as_view(), name='admin'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
