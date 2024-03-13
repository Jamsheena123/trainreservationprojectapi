from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_type_choices=[
        ('station', 'station'),
        ('Customer' ,'Customer'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='station')
    phone=models.CharField(max_length=10,null=True)
    

class Station(CustomUser):
    name = models.CharField(max_length=255)
    station_code=models.CharField(max_length=100,null=True)
    Location = models.CharField(max_length=200,null=True)
    phone_number=models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class Customer(CustomUser):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email_address = models.EmailField()
    biodata = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name  
    

    
class Train(models.Model):
    train_name=models.CharField(max_length=200,null=True)
    train_number=models.CharField(max_length=200)
    source=models.CharField(max_length=200)
    destination=models.CharField(max_length=200)
    departure_time=models.DateTimeField()
    arrival_time=models.DateTimeField() 
    seat_capacity=models.PositiveIntegerField(default=70)
    amount_nonac = models.PositiveIntegerField(default=0)
    amount_ac = models.PositiveIntegerField(default=0)
    amount_sleeper = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.train_number
    
   
   
class Booking(models.Model):
    train_number= models.ForeignKey(Train, on_delete=models.CASCADE)
    user= models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking_time=models.DateTimeField(auto_now_add=True)
    options=(
        ("Non AC","Non AC"),
        ("AC","AC"),
        ("Sleeper","Sleeper"),
    )
    seat_type=models.CharField(max_length=100,choices=options,default="Sleeper")
    reserved_seats = models.IntegerField()
    reservation_date = models.DateTimeField(auto_now_add=True)
    booking_amount=models.PositiveIntegerField()
    seat_no=models.PositiveIntegerField(null=True,unique=True)
    choice=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled','Cancelled')
    ]
    booking_status=models.CharField(max_length=100,choices=choice,default="Pending")

class Payment(models.Model):
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,unique=True,null=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    options=(
        ('pending','pending'),
        ('completed','completed'),
        ('failed','failed'),
    )
    status = models.CharField(max_length=20, choices=options,default='completed')

           
class Refund(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.ForeignKey(Payment,on_delete=models.CASCADE)


class Cancellation(models.Model):
    reservation = models.OneToOneField(Booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cancellation_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()   

from django.core.validators import MinValueValidator,MaxValueValidator

class Feedback(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,unique=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comments = models.TextField()




  



