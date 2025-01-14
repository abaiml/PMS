from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(ParkingSlot)
admin.site.register(Booking)
admin.site.register(Transaction)

