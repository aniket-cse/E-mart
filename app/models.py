from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.
STATE_CHOICE=(
   ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
   ('Andhra pradesh','Andhra pradesh'),
   ('Arunachal Pradesh','Arunachal Pradesh'),
   ('Assam','Assam'),
   ('Bihar','Bihar'),
   ('Chandigarh','Chandigarh'),
   ('Chhattisgarh','Chhattisgarh'),
   ('Chhattisgarh','Chhattisgarh'),
   ('West Bangal','West Bangal'),
)
class Profile(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICE =(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),

)

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=2)
    # product_image=models.ImageField(upload_to='product_img')
    # file will be uploaded to MEDIA_ROOT / uploads
    upload_image = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #p---> capital here
    product=models.ForeignKey(Product , on_delete=models.CASCADE)
    # quantity cannot be negative
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price


STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    id=models.AutoField(primary_key=True) # this one give primary key issue
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
