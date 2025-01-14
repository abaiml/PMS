from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=5, choices=[('entry', 'Entry'), ('exit', 'Exit'),])
    hire_date = models.DateField()
    mobile_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_position_display()})"


class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)
    vehicle_type = models.CharField(max_length=10, choices=[('car', 'Car'),('bike', 'Bike')])

    def __str__(self):
        return f"{self.slot_number} ({self.get_vehicle_type_display()})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=254, null=True, blank=True)
    plate_number = models.CharField(max_length=20, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.customer_name} - {self.slot.slot_number}"


class Transaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Transaction for {self.booking.customer_name} - {self.amount}"