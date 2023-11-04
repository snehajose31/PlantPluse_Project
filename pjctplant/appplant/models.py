from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','username']

    class Role (models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        CUSTOMER = "CUSTOMER",'CUSTOMER'
        BOTANIST = "BOTANIST", 'BOTANIST'
        HORTICULTURE = "HORTICULTURE", 'HORTICULTURE'
    role = models.CharField(max_length=50, choices= Role.choices)
        
    
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=11)
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default= 0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))
    product_image = models.ImageField(upload_to='product_images/')
    
    def save(self, *args, **kwargs):
    # Convert self.discount to a float and then calculate the sale price
     self.discount = float(self.discount)
     self.sale_price = self.price - (self.price * (self.discount / 100))
     super(Product, self).save(*args, **kwargs)

    def _str_(self):
        return self.product_name
