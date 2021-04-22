from django.urls import path
from .views.scan_views import Scans, ScanDetail, ScanApiDetail
from .views.item_views import Items, ItemDetail, ItemGetDetail
from .views.test_item_views import TestItems, TestItemsDetail, TestItemsGetDetail
from .views.material_views import Materials
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword, Admin, AdminDetail

urlpatterns = [
    # Restful routing

    path('items/', Items.as_view(), name='items'),
    path('update-item/', ItemDetail.as_view(), name='items'),
    path('items/<int:pk>', Items.as_view(), name='items'),
    path('materials/', Materials.as_view(), name='materials'),
    path('item/<int:pk>', ItemGetDetail.as_view(), name='items'),

    # scan routes
    path('scans/', Scans.as_view(), name='scans'),
    path('scans/<int:pk>/', ScanDetail.as_view(), name='scan_detail'),
    path('scan-item/<str:slug>/', ItemDetail.as_view(), name='scan_detail'),
    path('scan-item/<str:slug>/api/', ScanApiDetail.as_view(), name='scan_detail'),

    # User routes
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('users/<int:pk>/', AdminDetail.as_view(), name='admin'),
    path('users/', Admin.as_view(), name='admin'),
    path('change-password/', ChangePassword.as_view(), name='change-pw'),

    # Paths for my test admin
    path('test-items/', TestItems.as_view(), name='items'),
    path('update-test-item/', TestItemsDetail.as_view(), name='items'),
    path('test-item/<int:pk>', TestItemsGetDetail.as_view(), name='items'),
    path('test-items/<int:pk>', TestItems.as_view(), name='items'),
]
