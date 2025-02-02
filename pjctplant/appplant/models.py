from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
    


    
# class Product1(models.Model):
    
#     product_name = models.CharField(max_length=255)
#     category = models.ForeignKey(Category1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Category
#     subcategory = models.ForeignKey(Subcategory1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Subcategory
#     stock = models.PositiveIntegerField(default=1, null=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
#     sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     product_image = models.ImageField(upload_to='product_images/')
#     STATUS_CHOICES = [
#         ('In Stock', 'In Stock'),
#         ('Out of Stock', 'Out of Stock'),
#     ]

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

#     def save(self, *args, **kwargs):
#         # Update the status based on the quantity value
#         if self.stock == 0:                                                                                                                                                                 
#             self.status = 'Out of Stock'
#         else:
#             self.status = 'In Stock'

#         # Convert self.discount to a float and then calculate the sale price
#         self.discount = float(self.discount)  # Convert to float
#         self.price = float(self.price)  # Convert to float
#         self.sale_price = self.price - (self.price * (self.discount / 100))

#         super(Product1, self).save(*args, **kwargs)


#     def str(self):
#         return self.product_name







# class Product(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     product_name = models.CharField(max_length=255)
#     category = models.CharField(max_length=100)
#     subcategory = models.CharField(max_length=100)
#     quantity = models.PositiveIntegerField()
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=5, decimal_places=2, default= 0.0)
#     sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))
#     product_image = models.ImageField(upload_to='product_images/')
    
#     def save(self, *args, **kwargs):
#     # Convert self.discount to a float and then calculate the sale price
#      self.discount = float(self.discount)
#      self.sale_price = self.price - (self.price * (self.discount / 100))
#      super(Product, self).save(*args, **kwargs)

#     def _str_(self):
#         return self.product_name




# class AddToCart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product1, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def _str_(self):
#      return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"
 
# class AddToCart2(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product1, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def _str_(self):
#      return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"
 
# class WishlistItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey('Product1', on_delete=models.CASCADE)

    
    # def _str_(self):
    #      return self.product.product_name
     
# class cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product1, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def _str_(self):
#      return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"


class Category2(models.Model):
    name = models.CharField(max_length=100)
    def _str_(self):
        return self.name
     
class Subcategory2(models.Model):
     name = models.CharField(max_length=100)
     category = models.ForeignKey(Category2, on_delete=models.CASCADE)

     def _str_(self):
         return self.name
     
     
class Product2(models.Model):
    
     product_name = models.CharField(max_length=255)
     category = models.ForeignKey(Category2, on_delete=models.CASCADE)  # Use ForeignKey to relate to Category
     subcategory = models.ForeignKey(Subcategory2, on_delete=models.CASCADE)  # Use ForeignKey to relate to Subcategory
     stock = models.PositiveIntegerField(default=1, null=True)
     description = models.TextField()
     price = models.DecimalField(max_digits=10, decimal_places=2)
     discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
     sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
     product_image = models.ImageField(upload_to='product_images/')
     STATUS_CHOICES = [
         ('In Stock', 'In Stock'),
         ('Out of Stock', 'Out of Stock'),
     ]

     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

     def save(self, *args, **kwargs):
         # Update the status based on the quantity value
         if self.stock == 0:                                                                                                                                                                 
             self.status = 'Out of Stock'
         else:
             self.status = 'In Stock'

         # Convert self.discount to a float and then calculate the sale price
         self.discount = float(self.discount)  # Convert to float
         self.price = float(self.price)  # Convert to float
         self.sale_price = self.price - (self.price * (self.discount / 100))

         super(Product2, self).save(*args, **kwargs)


     def str(self):
         return self.product_name
     
     
class AddToCart3(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Product2, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)
     date_added = models.DateTimeField(auto_now_add=True)
     is_active = models.BooleanField(default=True)

     def _str_(self):
      return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"
  
  
class WishlistItem3(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey('Product2', on_delete=models.CASCADE)

    
     def _str_(self):
          return self.product.product_name
      


class Botanist(models.Model):
    name = models.CharField(max_length=255)
    # Add more fields as needed, e.g., qualification, specialty, experience, etc.

    def __str__(self):
        return self.name
    
    
    
#appointment
class DoctorSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.user.username} - {self.date} - {self.time_slot}"

class Appointment(models.Model):
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)
    botanist = models.ForeignKey(Botanist, on_delete=models.CASCADE)
    subject = models.TextField()

    def __str__(self):
        return f"Appointment with {self.botanist.name} on {self.appointment_date} at {self.appointment_time}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()  # Add this line to include the email field
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)  # Assuming address is optional
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username
    
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product2, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product2, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product2, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)  # New field for order cancellation
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    def cancel(self):
        # Add your cancellation logic here
        self.cancelled = True  # Mark the order as cancelled
        self.save()  # Save the changes to the database
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product2, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
    
class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)  # New field
    state = models.CharField(max_length=50, blank=True, null=True)  # New field

    def __str__(self):
        return self.user.username    
    
    
class BotProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    specification = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=8, decimal_places=2) 
    
    def __str__(self):
        return self.user.username  
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # Add a description field
    video_file = models.FileField(upload_to='videos/')
    # Add any other fields you need, such as tags, etc.

    def _str_(self):
        return self.title
    
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.title



class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
    
class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirm', 'Confirmed'),
        ('complete', 'Complete'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.service} - {self.status}"
    
class ServiceRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    bot_profile = models.ForeignKey(BotProfile, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirm', 'Confirmed'),
        ('complete', 'Complete'),
        ('reject', 'reject'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.service} - {self.status}"
    
    
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)
    method = models.CharField(max_length=50, choices=(("online", "Online"), ("offline", "Offline")))
    reason = models.TextField()
    fees = models.ForeignKey(BotProfile, on_delete=models.CASCADE, null=True, default=None)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.doctor_schedule.date} - {self.doctor_schedule.time_slot}"
    
class BotanistWork(models.Model):
    botanist_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='botanist_work_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class BotanistWorks(models.Model):
   
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='botanist_work_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    
class BotanistWorkk(models.Model):
    botanist = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='botanist_work/', blank=True)
    
    def __str__(self):
        return f"{self.botanist.user.username}'s Work: {self.title}"

class CustomerPhoto(models.Model):
    photo = models.ImageField(upload_to='customer_photos/')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    chosen_botanist = models.ForeignKey(BotProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo submitted by {self.submitted_by.username} at {self.submitted_at}'
   
    
class Itemss(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    image = models.ImageField(upload_to='images1/')
    description = models.TextField(null=True)

    def __str__(self):
        return self.title