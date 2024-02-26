from django.contrib import admin

from Stationapi.models import Train,Booking,Feedback,Payment

# Register your models here.

admin.site.register(Train)
admin.site.register(Booking)
admin.site.register(Feedback)
admin.site.register(Payment)
