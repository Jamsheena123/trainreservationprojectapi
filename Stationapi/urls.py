from django.urls import path
from Stationapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("train",views.TrainView,basename="trains")
router.register("traincapacity",views.TrainCapacityView,basename="train_seats")


urlpatterns=[
    path("register/",views.StationCreationView.as_view(),name="signin"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    
]+router.urls