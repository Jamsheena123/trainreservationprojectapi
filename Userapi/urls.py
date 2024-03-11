from django.urls import path
from Userapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt


router=DefaultRouter()
router.register("train",views.TrainView,basename="trains"),
router.register("bookinghistory",views.BookTicketView,basename="history"),

urlpatterns=[
    path("signup/",views.CustomerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("profile/",views.UserProfileView.as_view(),name="profile"),
    path('train_status/',views.search_trains_view, name='train_status_api'),

    


    # path('trains/<int:pk>/cancel_reservation/', TrainView.as_view({'post': 'cancel_reservation'}), name='cancel-reservation'),


    

] +router.urls