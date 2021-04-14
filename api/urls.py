from django.urls import path
from .views.scan_views import Scans, ScanDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('scans/', Scans.as_view(), name='scans'),
    path('scans/<int:pk>/', ScanDetail.as_view(), name='scan_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
