from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login as klogin,logout
from django.contrib import messages
from . models import User
from django.template import RequestContext
# from django.http import HttpResponse
#from . models import Product
from . models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import *
from django.contrib.auth.decorators import *
from .forms import AppointmentForm




from .models import Product2, Cart, CartItem
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def registration(request):
     if request.method == 'POST':
        #name = request.POST.get('name', None)
        username = request.POST['username']
        email = request.POST['email']
        #phone = request.POST.get('phone', None)
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role='CUSTOMER'
        # role = CustomUser.CUSTOMER
        if username and email  and password:
            if User.objects.filter(email=email,username=username).exists():
                messages.success(request,("Email is already registered."))
            
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                User.objects.create_user(username=username, email=email, password=password,role=role)
                # activateEmail(request, user, email)
                return redirect('login')  
     return render(request, 'registration.html')
   

from .models import User  # Import your User model from your app

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_authenticated:
                klogin(request, user)
                
                if user.role == User.Role.CUSTOMER:
                    return redirect('home')
                elif user.role == User.Role.BOTANIST:
                    return redirect('consult')
                elif user.role == User.Role.ADMIN:
                    return redirect('/adminpanel/')
                elif user.role == User.Role.HORTICULTURE:
                    return redirect('horticulture')
                else:
                    messages.error(request, "Invalid role.")
                    return redirect('/login')

    return render(request, 'login.html')  # Render the login page



# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
        
#         # Authenticate using email and password
#         user = authenticate(request, username=email, password=password)
        
#         if user is not None:
#             if user.is_authenticated:
                
#                 print(user)
#                 if user is not None:
#                     klogin(request, user)
#                     if user.role == User.Role.ADMIN:  # Assuming you have a 'role' field to distinguish between users and admins
#                         # Log in the admin user
#                         return redirect('/adminpanel/')  # Redirect to the admin panel URL
#                     elif user.role == User.Role.CUSTOMER:  # Assuming you have a 'role' field to distinguish between users and admins
#                         # Log in the admin user
#                         return redirect('home')
#                     elif user.role == User.Role.BOTANIST:  # Assuming you have a 'role' field to distinguish between users and admins
#                         # Log in the admin user
#                         return redirect('consult')
#                     # else:
#                     #     request.session["useremail"] = user.email
#                     #     return redirect('/home')  # Redirect to the regular user's home page
#                 else:
#                     messages.error(request, "Invalid credentials.")
#                     return redirect('/login')
    
#     return render(request, 'login.html')  # Render the login page



def about(request):
    return render(request,'about.html')

@never_cache
@login_required(login_url='login')
def home(request):
    # Make sure you're not using a variable named 'user' here
    # Instead, use a different variable name, for example, 'current_user'
    current_user = request.user

    # Your view logic here

    return render(request, 'home.html', {'current_user': current_user})

# def home(request):
#     user = request.user
#     print(user) 
#     return render(request,'home.html',{'user':user})

def contact(request):
    return render(request,'contact.html')


def profile(request):
    user=request.user
    try:
        userinfo=UserProfile.objects.filter(user=user)
        if request.method == 'POST':
            full_name = request.POST.get('fullname')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date-of-birth')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            user_info = UserProfile(user=request.user, contact_no=phone, place='', city='', district='', pincode='')
        user_info.save()
         
    except:
         userinfo=UserProfile()   
    
    return render(request,'profile.html',{'userinfo':userinfo})

# def your_view(request):
#     # Your view logic here
#     return render(request, 'your_template.html', context_instance=RequestContext(request))

def adminpanel(request):
    return render(request,'adminpanel.html')

# from .models import Product2, Category2



def add_product(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category, created = Category2.objects.get_or_create(name=category_name)

        # Retrieve or create the Subcategory2 instance while providing the Category2 instance
        subcategory_name = request.POST.get('subcategory-name')
        subcategory, created = Subcategory2.objects.get_or_create(name=subcategory_name, category=category)

        # Handle the form submission
        product_name = request.POST.get('product-name')
        stock = request.POST.get('stock')  # Retrieve quantity from the form
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        price = float(price)
        discount = float(discount)

        # Calculate sale_price
        sale_price = price - (price * (discount / 100))

        # Create a new Product2 object and save it to the database
        product = Product2(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            stock=stock,  # Assign the quantity field
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,
            status=status,
            product_image=product_image,
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('viewproduct')

    return render(request, 'addproduct.html')





def view_product(request):
    # Assuming you have a queryset of products (e.g., Product.objects.all())
    products = Product2.objects.all()
    
    for product in products :
        queryset=Category2.objects.filter(id=product.category_id)
        queryset1=Subcategory2.objects.filter(id=product.subcategory_id)
        product.subcat=queryset1[0]
        product.procat = queryset[0]
    return render(request, 'viewproduct.html', {'products': products})

def product_grid(request):
    products = Product2.objects.all()  # Fetch all products
    return render(request, 'plants.html', {'products': products})

@never_cache
@login_required(login_url='login')
def user_r(request):
    user_s = User.objects.all()  # Fetch all products
    return render(request, 'user.html', {'user_s': user_s})

@never_cache
@login_required(login_url='login')
def botanist_t(request):
    return render(request,'botanist.html')


def hort(request):
    return render(request,'hort.html')

@never_cache
@login_required(login_url='login')
def bot_t(request):
    return render(request,'bot.html')

def custome_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
@never_cache
@login_required(login_url='login')
def delete_product(request, id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = Product2.objects.get(pk=id)
            product.delete()
            return redirect('viewproduct')
        except Product2.DoesNotExist:
            pass
    return redirect('viewproduct')  # Redirect back to the product list view

def product_details(request, id):
    # Retrieve the product details from the database
    product = get_object_or_404(Product2, pk=id)

    # Render the product details template with the product data
    return render(request, 'details.html', {'product': product})

def edit_product(request, id):
    product = get_object_or_404(Product2, pk=id)

    if request.method == 'POST':
        try:
            product_name = request.POST.get('product-name')
            category_id = request.POST.get('category-name')
            subcategory_id = request.POST.get('subcategory-name')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            price = request.POST.get('price')
            discount = request.POST.get('discount')# Retrieve as a string
            product_image = request.FILES.get('product_image')
            if product_image:
                product.product_image = product_image

            price = float(price)

            # Convert discount to a float
            discount = float(discount)

            
            

            # Calculate sale_price
            sale_price = price - (price * (discount / 100))

            # Create a new Product object and save it to the database
            product = Product2(
                #product_id=id,
                product_name=product_name,
                category=category_id,
                subcategory=subcategory_id,
                stock=stock,
                description=description,
                price=price,
                discount=discount,
                sale_price=sale_price,  # Assign the calculated sale price

                product_image=product_image
            )
            product.save()

            # Redirect to a success page or any other desired action
            return redirect('viewproduct') # Replace 'viewproduct' with the actual URL name

        except Exception as e:
            print(str(e))
            # Handle exceptions, such as validation errors
            # You can return an error message or render the form with error details
            return render(request, 'editproduct.html', {'product': product, 'error_message': str(e)})

    # If the request method is GET, render the edit product form
    return render(request, 'editproduct.html', {'product': product})






# def view_cart(request):
#     user=request.user
#     user_id = user.id
#     print(user_id)
#     cart_items = AddToCart3.objects.filter(user=user_id, is_active=True)

#     # Ensure the quantity is at least 1 and update the total price based on the quantity
#     for item in cart_items:
#         if item.product.stock < 1 or item.product.stock is None:
#             item.product.stock = 1  # Set the minimum quantity to 1
#         item.total_price = item.product.sale_price * item.product.stock # Update the total price based on the new quantity

#     # Calculate order summary
#     subtotal = sum(item.total_price for item in cart_items)
#     shipping = 5  # Adjust this value as needed
#     total = subtotal + shipping

#     context = {
#     'cart_items': cart_items,
#     'subtotal': subtotal,
#     'shipping': shipping,
#     'total': total,
#     'total_amount': total,  # Add the total amount to the context
# }

#     return render(request, 'view_cart.html', context)

# def add_to_cart(request, id):
#     # Retrieve the product based on its ID (you should have a Product model)
#     product = Product2.objects.get(pk=id) 
#     user=request.user
#     email=user.email
#     user = get_object_or_404(User, email=email)
    
#         # Check if the user already has this product in their cart
#     cart_item = AddToCart3(user=user, product=product)  # You can set the quantity as neede
#     cart_item.save()
#     print(cart_item)
#     return redirect('view_cart') 

@never_cache
@login_required(login_url='login')
def flowering_plants(request):
    flowering_plants = Product2.objects.filter(category_id="1", subcategory_id='1')
    return render(request, 'flowering_plants.html', {'products': flowering_plants})

# def flowering_plants(request):
#     # Retrieve products under the "flowering plants" subcategory
#     flowering_plants = Product2.objects.filter(category_id="1", subcategory_id='1')
#     print(flowering_plants)  # Add this line for debugging

#     return render(request, 'flowering_plants.html', {'products': flowering_plants})

@never_cache
@login_required(login_url='login')
def medicinal_plants(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    medicinal_plants = Product2.objects.filter(category="1", subcategory='2')
    return render(request, 'medicinal_plants.html', {'products': medicinal_plants})
@never_cache
@login_required(login_url='login')
def organic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    organic = Product2.objects.filter(category="2", subcategory='4')
    
    
    return render(request, 'organic.html', {'products': organic})
@never_cache
@login_required(login_url='login')
def inorganic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    inorganic = Product2.objects.filter(category="2", subcategory='3')
    
    
    return render(request, 'inorganic.html', {'products': inorganic})
@never_cache
@login_required(login_url='login')
def vegetable_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    vegetable_seed = Product2.objects.filter(category="3", subcategory='5')
    
    
    return render(request, 'vegetable_seed.html', {'products': vegetable_seed})
@never_cache
@login_required(login_url='login')
def flowering_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    flowering_seed = Product2.objects.filter(category="seed", subcategory='flowering seed')
    
    
    return render(request, 'floweringseed.html', {'products': flowering_seed})
@never_cache
@login_required(login_url='login')
def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product2.objects.filter(product_name__icontains=query)
    else:
        products = Product2.objects.all()
    
    return render(request, 'flowering_plants.html', {'products': products})


def regbot(request):
     if request.method == 'POST':
        #name = request.POST.get('name', None)
        username = request.POST['username']
        email = request.POST['email']
        #phone = request.POST.get('phone', None)
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role='BOTANIST'
        if username and email  and password:
            if User.objects.filter(email=email,username=username).exists():
                messages.success(request,("Email is already registered."))
            
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                User.objects.create_user(username=username, email=email, password=password,role=role)
                return redirect('login')  
     return render(request, 'regibot.html')
 
def reghorti(request):
     if request.method == 'POST':
        #name = request.POST.get('name', None)
        username = request.POST['username']
        email = request.POST['email']
        #phone = request.POST.get('phone', None)
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role='HORTICULTURE'
        if username and email  and password:
            if User.objects.filter(email=email,username=username).exists():
                messages.success(request,("Email is already registered."))
            
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                User.objects.create_user(username=username, email=email, password=password,role=role)
                return redirect('login')  
     return render(request, 'reghorti.html')
 
 
 
def consult(request):
    return render(request,'consult.html')


def book(request):
    return render(request,'book.html')

# def book_appointment(request):
#     return render(request, 'book-appointment.html')

def botdetail(request):
    return render(request,'botdetail.html')

# views.py


from .models import Botanist, Appointment
from django.http import HttpResponse

# def consultation_form(request):
#     if request.method == 'POST':
#         selected_date = request.POST.get('appointment-date')
#         selected_time = request.POST.get('appointment-time')
#         selected_botanist_id = request.POST.get('botanist')
#         subject = request.POST.get('subject')

#         # Validate the form data
#         if selected_date and selected_time and selected_botanist_id and subject:
#             try:
#                 selected_botanist = Botanist.objects.get(pk=selected_botanist_id)

#                 # Save the appointment to the database
#                 appointment = Appointment(
#                     appointment_date=selected_date,
#                     appointment_time=selected_time,
#                     botanist=selected_botanist,
#                     subject=subject
#                 )
#                 appointment.save()

#                 # Redirect to the botanist.html page
#                 return redirect('botanist_page')  # Replace 'botanist_page' with the actual name or URL pattern of your botanist.html page
#             except Botanist.DoesNotExist:
#                 # Handle the case where the selected botanist does not exist
#                 return HttpResponse("Invalid botanist selected.")
#         else:
#             # Handle the case where form data is incomplete
#             return HttpResponse("Please fill out all fields before scheduling the appointment.")
#     else:
#         # Retrieve botanists from the database to populate the form
#         botanists = Botanist.objects.all()

#         context = {
#             'botanists': botanists,
#         }

#         return render(request, 'book-appointment.html', context)
def consultation_form(request,id):
    schedule = DoctorSchedule.objects.filter(user_id = id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
    else :
        form = AppointmentForm()
    context = {'form' :form,
               'schedules' : schedule
               }
    return render(request, 'book-appointment.html', context)

from .forms import BookForm

def confirm(request,id):
    doctorSchedule = DoctorSchedule.objects.get(id =id)
    profile = BotProfile.objects.get(user = doctorSchedule.user)
    if request.method == 'POST':
        user = request.user
        form = BookForm(request.POST)
        if form.is_valid():
            method =request.POST['method']
            reason =request.POST['reason']
            book_instance = Book.objects.create(
                user=user,
                doctor_schedule=doctorSchedule,
                method=method,
                reason=reason,
                fees = profile
            )
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(book_instance.fees.fee * 100),
                'currency': 'INR',
                'receipt': f'order_{book_instance.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            book_instance.payment_id = orderData['id']
            book_instance.save()
            return redirect('con_pay', book_id=book_instance.id)
    else:
        form = BookForm()
    return render(request, 'confirm.html', {'form': form,'doctorSchedule': doctorSchedule ,
                                            'profile':profile})
    
def con_pay(request,book_id):
    book = Book.objects.get(id = book_id)
    return render(request,'pay_confirm.html',{'book':book})
    

def search_user(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()

    context = {'user_s': users}
    return render(request, 'user.html', context)


def works(request):
    return render(request,'work.html')



# def remove_from_cart(request, item_id):
#     item = get_object_or_404(AddToCart3, pk=item_id)

#     if item.user == request.user:
#         # Remove the item from the cart and the database
#         item.delete()

#     # Recalculate order summary after item removal
#     cart_items = AddToCart3.objects.filter(user=request.user, is_active=True)
#     subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
#     shipping = 10  # Adjust this value as needed
#     total = subtotal + shipping

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'total': total,
#     }
#     return render(request, 'view_cart.html', context)



def deactivate_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    # Perform deactivation logic (e.g., set user.is_active to False)
    user.is_active = False
    user.save()

    messages.success(request, f"{user.username} has been deactivated.")
    return redirect('adminpanel') 


def activate_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    # Perform activation logic (e.g., set user.is_active to True)
    user.is_active = True
    user.save()

    messages.success(request, f"{user.username} has been activated.")
    return redirect('adminpanel')




# def wishlist(request):
#     if request.user.is_authenticated:
#         wishlist_items = WishlistItem3.objects.filter(user=request.user)
#         return render(request, 'wish.html', {'wishlist_items': wishlist_items})
#     else:
#         return redirect('login')  # Redirect to the login page if the user is not authenticated

# def add_to_wishlist(request, id):
#     if request.user.is_authenticated:
#         product = Product2.objects.get(id=id)
#         wishlist_item, created = WishlistItem3.objects.get_or_create(user=request.user, product=product)
#         if created:
#             # The item was added to the wishlist
#             messages.success(request, f'{product.product_name} has been added to your wishlist.')
#         else:
#             # The item is already in the wishlist
#             messages.warning(request, f'{product.product_name} is already in your wishlist.')
#     return redirect('wish')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product2, WishlistItem3

def wishs(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem3.objects.filter(user=request.user)
        return render(request, 'wish.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = Product2.objects.get(id=id)
        wishlist_item, created = WishlistItem3.objects.get_or_create(user=request.user, product=product)
        if created:
            # The item was added to the wishlist
            messages.success(request, f'{product.product_name} has been added to your wishlist.')
        else:
            # The item is already in the wishlist
            messages.warning(request, f'{product.product_name} is already in your wishlist.')
    return redirect('wish')

# your_app/views.py

from django.shortcuts import render
from .models import User

def pf(request):
    # Assuming the user is authenticated
    user = request.user

    # Pass the user's name and email to the template context
    context = {
        'user_fullname': user.username,
        'user_email': user.email,
    }

    return render(request, 'profile.html', context)


def delete_from_wishlist(request, id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(WishlistItem3, user=request.user, product__id=id)
        product_name = wishlist_item.product.product_name  # Store the product name for the message
        wishlist_item.delete()
        messages.success(request, f'{product_name} has been removed from your wishlist.')
    else:
        messages.warning(request, 'You must be logged in to remove items from your wishlist.')

    return redirect('wish')




from django.shortcuts import render, redirect
from .models import UserProfile




from django.http import HttpResponseRedirect
import datetime


def profile1(request):
    user=request.user
    try:
        user_info=UserProfile.objects.filter(user=user)
        if request.method == 'POST':
            full_name = request.POST.get('fullname')
            gender = request.POST.get('gender')
            date_of_birth_str = request.POST.get('date-of-birth')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            user_info = UserProfile(user=request.user,name=full_name,email = email,gender = gender,date_of_birth = date_of_birth_str, address = address,phone = phone)
        user_info.save()
         
    except:
         userinfo=UserProfile()   
         if request.method == 'POST':
            userinfo.user =request.user
            userinfo.gender = request.POST.get('gender')
            userinfo.date_of_birth_str = request.POST.get('date-of-birth')
            userinfo.address = request.POST.get('address')
            userinfo.email = request.POST.get('email')
            userinfo.phone = request.POST.get('phone')
            userinfo.save
         
    # user = request.user
    # try:
    #     user_profile = UserProfile.objects.get(user=user)
    # except UserProfile.DoesNotExist:
    #     user_profile = UserProfile(user=user)

    # if request.method == 'POST':
    #     full_name = request.POST.get('fullname')
    #     gender = request.POST.get('gender')
    #     date_of_birth_str = request.POST.get('date-of-birth')
    #     address = request.POST.get('address')
    #     email = request.POST.get('email')
    #     phone = request.POST.get('phone')

    #     # Attempt to convert the date of birth string to a datetime.date object
    #     try:
    #         date_of_birth = datetime.datetime.strptime(date_of_birth_str, '%m/%d/%Y').date()
    #     except ValueError:
    #         # Handle the case where the date format is incorrect
    #         date_of_birth = None

    #     # Update or create the UserProfile instance
    #     user_profile.full_name = full_name
    #     user_profile.gender = gender
    #     user_profile.date_of_birth = date_of_birth
    #     user_profile.address = address
    #     user_profile.email = email
    #     user_profile.phone = phone

    #     user_profile.save()

    #     # Redirect to the profile page after saving
    #     return HttpResponseRedirect('/profile')

    return render(request, 'profile.html', {'UserProfile': user_info})



# def checkout(request):
#     # Assuming you have a function to calculate total in your models or views
#     total = calculate_total(request.user)  # Replace with your own logic

#     if request.method == 'POST':
#         # Assuming you have a form for the checkout details
#         # Replace 'YourCheckoutForm' with the actual form class
#         form = YourCheckoutForm(request.POST)

#         if form.is_valid():
#             # Process the order, save the details, etc.
#             # You may need to create a new Order model and save the order details there
#             # This is just a placeholder code
#             name = form.cleaned_data['name']
#             gender = form.cleaned_data['gender']
#             dob = form.cleaned_data['dob']
#             email = form.cleaned_data['email']
#             address = form.cleaned_data['address']
#             phone = form.cleaned_data['phone']

#             # Redirect to a thank you page or order confirmation page
#             messages.success(request, 'Order placed successfully!')
#             return redirect('order_confirmation')
#     else:
#         form = YourCheckoutForm()  # Replace with the actual form class

#     # Get the items in the cart for the order summary
#     cart_items = AddToCart3.objects.filter(user=request.user)  # Replace with your own logic

#     return render(request, 'yourapp/checkout.html', {'form': form, 'cart_items': cart_items, 'total': total})
# def checkout(request):
#      # Fetch the cart items for the current user
#      cart_items = AddToCart3.objects.filter(user=request.user)

#     # Calculate the total amount (you may already have a function for this)
#      total = sum(item.quantity * item.product.price for item in cart_items)

# #     # Other logic for processing the checkout form, if needed

#      return render(request, 'checkot.html', {'cart_items': cart_items, 'total': total})




def log1(request):
    return render(request,'log.html')


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')  # Get the old password from the form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user  # Get the currently logged-in user

        # Check if the entered old password matches the user's current password
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            # Change the user's password and save it to the database
            user.set_password(new_password)
            user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')



def add_to_cart(request, id):
    product = Product2.objects.get(pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')


def remove_from_cart(request, id):
    product = Product2.objects.get(pk=id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('view_cart')

def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.sale_price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items,'total_amount': total_amount})

def increase_cart_item(request, id):
    product = Product2.objects.get(pk=id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')

def decrease_cart_item(request, id):
    product = Product2.objects.get(pk=id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')


def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})



def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        
        
        
@csrf_exempt
def create_order1(request):
    if request.method == 'POST':
        user = request.user
        last_item = Book.objects.filter(user=user).last()
        total_amount = last_item.fees.fee
        try:
            # order = Order.objects.create(user=user, total_amount=last_item)
            # for cart_item in cart_items:
            #     OrderItem.objects.create(
            #         order=order,
            #         product=cart_item.product,
            #         quantity=cart_item.quantity,
            #         item_total=cart_item.product.price * cart_item.quantity
            #     )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int( total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{last_item.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            last_item.payment_id = orderData['id']
            last_item.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred1. Please try again.'}, status=500)

        
def checkout(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)
    email = request.user.email
    full_name = request.user.username

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email':email,
        'full_name': full_name
    }
    return render(request, 'checkot.html', context)

def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                user = request.user
                user.cart.cartitem_set.all().delete()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})
        
        
        

def handle_payment1(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order =Book.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})

#user profile

def user_profile(request):
    # Retrieve the logged-in user's information
    user = request.user

    # You can fetch additional information from the user's profile if needed
    # For example: profile = user.profileuser

    context = {
        'user': user,
        # Add additional context variables as needed
    }

    return render(request, 'user_profile.html', context)






def save_profile(request):
    if request.method == 'POST':
        try:
            # Retrieve the user's profile instance or create it if it doesn't exist
            user_profile, created = ProfileUser.objects.get_or_create(user=request.user)

            # Get form data from the request
            phone_number = request.POST.get('phone_number')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            state = request.POST.get('state')

            # Update the user's profile fields
            user_profile.phone_number = phone_number
            user_profile.pincode = pincode
            user_profile.address = address
            user_profile.gender = gender
            user_profile.city = city
            user_profile.state = state

            # Save the changes
            user_profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')  # Redirect to the user profile page
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')

    return render(request, 'user_profile.html')




def order_complete(request):
    order_id = request.GET.get('order_id')
    transID = request.GET.get('payment_id')
    print("Order ID from GET parameters:", order_id)
    try:
   
        order = Order.objects.get(id=order_id, payment_status=True)
        print("Retrieved Order:", order)
        ordered_products = OrderItem.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product.sale_price * i.quantity
        

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_id': order.id,
           'transID': transID,
           'subtotal': subtotal,
        }

        return render(request, 'order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('order_complete')


# def user_profile(request):
#     # Assuming you have a template named 'userdetails.html' in the 'templates' folder
#     return render(request, 'user_profile.html', {'user': request.user})

@never_cache
@login_required(login_url='login')
def bill_invoice(request):
    # Fetch the latest order for the logged-in user (or implement your logic)
    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'billinvoice.html', {'order': order})

@never_cache
@login_required(login_url='login')
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'order_history.html', {'orders': orders})

@never_cache
@login_required(login_url='login')
def search_prod(request):
    query = request.GET.get('q', '')
    products = Product2.objects.filter(product_name=query)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'viewproduct.html', context)

def horti(request):
    return render(request,'horti.html')


def horticulture(request):
    return render(request,'horticulture.html')

#appointment

def scheduling(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        

        # Check if the date and time slot are present in the POST request
        if not date or not time_slot:
            messages.error(request, 'Please select a date and time slot.')
        else:
            # Check if the user is a doctor
            if request.user.role == 'BOTANIST':
                # Check if the schedule already exists for the given date and time slot
                existing_schedule = DoctorSchedule.objects.filter(user=request.user, date=date, time_slot=time_slot)
                if existing_schedule.exists():
                    messages.error(request, 'Schedule already exists for this date and time slot.')
                else:
                    # If not, create and save the schedule
                    schedule = DoctorSchedule.objects.create(user=request.user, date=date, time_slot=time_slot)
                    schedule.save()
            else:
                # Handle the case when the user is not a doctor
                messages.error(request, 'You are not a registered doctor.')

    # Fetch existing schedules for the current doctor
    doctor_schedules = DoctorSchedule.objects.filter(user=request.user)

    return render(request, 'appoint.html', {'doctor_schedules': doctor_schedules})

def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(DoctorSchedule, id=schedule_id)
    schedule.delete()
    return redirect('scheduling')


def get_time_slots(request, selected_date):
    doctor_id = request.GET.get('user_id')
    doctor = get_object_or_404(User, id=doctor_id, role='Doctor')

    # Fetch available and booked time slots for the selected date and doctor
    available_time_slots = DoctorSchedule.objects.filter(user=doctor, date=selected_date).values_list('time_slot', flat=True)
    booked_time_slots = Appointment.objects.filter(doctor=doctor, date=selected_date).values_list('time_slot', flat=True)

    # Convert the QuerySets to lists and return as JSON
    return JsonResponse({'available': list(available_time_slots), 'booked': list(booked_time_slots)})


#bot profile
def save_profile(request):
    if request.method == 'POST':
        user = request.user
        user.profile.phone_number = request.POST.get('phone_number')
        user.profile.pincode = request.POST.get('pincode')
        user.profile.address = request.POST.get('address')
        user.profile.gender = request.POST.get('gender')
        user.profile.city = request.POST.get('city')
        user.profile.state = request.POST.get('state')
        user.profile.specification = request.POST.get('specification')  # Add this line
        user.profile.fee = request.POST.get('fee')
        print(request.POST.get('fee')) 
        
        user.profile.save()
        return redirect('bot_profile')
    else:
        return redirect('bot_profile')


def bot_profile(request):
    return render(request,'bot_profile.html')


def save_profile1(request):
    # print('///////////////////////////////////////////////////////////////////////////////')
    if request.method == 'POST':
            # Retrieve the user's profile instance or create it if it doesn't exist
            user_profile =BotProfile.objects.get(user=request.user)
            

            # Get form data from the request
            phone_number = request.POST.get('phone-number')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            state = request.POST.get('state')
            specification = request.POST.get('specification')
            fee = request.POST.get('fee')  # Add this line for the fee field
            print( phone_number )
            # Update the user's profile fields
            user_profile.phone_number = phone_number
            user_profile.pincode = pincode
            user_profile.address = address
            user_profile.gender = gender
            user_profile.city = city
            user_profile.state = state
            user_profile.specification = specification
            user_profile.fee = fee

            # Save the changes
            user_profile.save()

            messages.success(request, 'Profile updated successfully.')
    return render(request, 'user_profil.html')



def user_profil(request):
    user = request.user
    print(user)
    return render(request,'user_profil.html')

def botanist_list(request):
    botanists = BotProfile.objects.all()
    return render(request, 'botanist_list.html', {'botanists': botanists})



from .forms import VideoForm

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('horticulture')  # Update with your template name
    else:
        form = VideoForm()
    
    return render(request, 'upload_video.html', {'form': form})

from .models import Video

def display_videos(request):
    videos = Video.objects.all()
    return render(request, 'display_videos.html', {'videos': videos})


# #chatgpt nrs
#      # chatapp/views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# @csrf_exempt
# def chatgpt(request):
#     return render(request, 'chatgpt.html')

# @csrf_exempt
# def generate_response(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')
#         response = generate_gpt2_response(user_input)
#         return JsonResponse({'response': response})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

# def generate_response(request):
#     if request.method == 'POST':

#         user_input = request.POST.get('user_input').lower()
#         if 'plantpulse' in user_input:
#             response_data = {'response': "Plantpulse is an innovative web-based forum designed to cater to the diverse needs and interests of plant enthusiasts, including gardeners, product purchasers, and experts! How can I assist you today?"}
#         elif 'products' in user_input:
#             response_data = {'response': "We offer a wide range of vegetable seed, medicinal plant, flowering plant, and more. Browse our collection online!"}
#         elif 'hi' in user_input:
#             response_data = {'response': "hellooo"}
#         elif 'servies' in user_input:
#             response_data = {'response': "Plantpulse provides e-commerce, consultations,  plant development assistance, knowledge sharing, and disease management services. "}
#         elif 'botanist' in user_input:
#             response_data = {'response': "Expert advice on plant care, pest management, and disease prevention."}
#         elif 'How do Botanists ensure plant quality?' in user_input:
#             response_data = {'response': "Utilizing advanced features such as automated disease detection "}
#         elif ' Horticulture Experts' in user_input:
#             response_data = {'response': "Assistance in plant development, tutorials, blogs, and live alerts."}
#         elif 'offers' in user_input or 'discounts' in user_input:
#             response_data = {'response': "Check out our latest offers and discounts on premium beauty products. Don't miss out on great deals!"}
#         elif 'order' in user_input or 'delivery' in user_input:
#             response_data = {'response': "For information about your order or delivery, please contact our customer support at support@beautecart.com."}
#         else:
            
#             response_data = {'response': "Sorry Idk"}
#             # response = generate_gpt2_response(user_input)
#             # response_data = {'response': response}

#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

# def generate_gpt2_response(user_input, max_length=100):
#     input_ids = tokenizer.encode(user_input, return_tensors="pt")
#     output = model.generate(input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response



#botanist list
def user_list(request):
    botprofiles = BotProfile.objects.all()
    return render(request, 'user_list.html', {'botprofiles': botprofiles})

def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('user_list')

#video
from .models import Video

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    return redirect('video_list')  # Redirect to video list page

from .models import Video

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})


def edit_video(request, video_id):
    # Fetch video details based on video_id and pass it to the template
    video = Video.objects.get(id=video_id)
    return render(request, 'edit_video.html', {'video': video})

from django.core.files.base import ContentFile
import os

def save_edits(request, video_id):
    if request.method == 'POST':
        # Fetch the video instance
        video = Video.objects.get(id=video_id)

        # Update title and description
        video.title = request.POST.get('title')
        video.description = request.POST.get('description')

        # Handle video file upload
        if 'video_file' in request.FILES:
            # Delete the existing video file if it exists
            if video.video_file:
                os.remove(video.video_file.path)
            # Get the new video file from the request
            video_file = request.FILES['video_file']
            # Save the new video file
            video.video_file.save(video_file.name, video_file)

        # Save the updated video
        video.save()

        # Redirect back to the videos page
        return redirect('videos')

from .forms import PostForm

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consult')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


from .models import Post

def post(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})

def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
    return redirect('post')

from .models import DoctorSchedule

def reschedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('reschedule_schedule')
        new_date = request.POST.get('new_date')
        new_time_slot = request.POST.get('new_time_slot')
        
        # Update the schedule with the new date and time slot
        schedule = DoctorSchedule.objects.get(id=schedule_id)
        schedule.date = new_date
        schedule.time_slot = new_time_slot
        schedule.save()
        
        return redirect('consult')  # Redirect to the home page or any other appropriate page after rescheduling
        
    # If not a POST request, render the reschedule form
    doctor_schedules = DoctorSchedule.objects.all()
    return render(request, 'reschedule.html', {'doctor_schedules': doctor_schedules})

# from .models import DoctorSchedule

# def scheduling(request):
#     if request.method == 'POST':
#         date = request.POST.get('date')
#         time_slots = request.POST.getlist('time_slots[]')

#         # Save the schedule to the database
#         for slot in time_slots:
#             schedule = DoctorSchedule(date=date, time_slot=slot)
#             schedule.save()

#         return JsonResponse({'success': True})

#     # Handle GET request if needed
#     return render(request, 'scheduling_form.html', context={})


from django.shortcuts import render, redirect
from .models import DoctorSchedule
from django.http import HttpResponse

def scheduling_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slots = request.POST.getlist('time_slot')
        
        # Create DoctorSchedule objects for each selected time slot
        for time_slot in time_slots:
            schedule = DoctorSchedule(date=date, time_slot=time_slot)
            schedule.save()
        
        return HttpResponse('Schedules added successfully!')
    else:
        return HttpResponse('Invalid request method.')

# Define your other views here...



from .models import Service
from .forms import ServiceForm

def service_list(request):
    services = Service.objects.all()
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    return render(request, 'service_list.html', {'services': services, 'form': form})


def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')

from .forms import ServiceRequestsForm

from .forms import ServiceRequestsForm

def service_request_form(request):
    
    if request.method == 'POST':
        form = ServiceRequestsForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            messages.success(request, 'Service request submitted successfully!')
            return redirect('service_request_form')  # Redirect to the same page
    else:
        
        form = ServiceRequestsForm()
    user=request.user
    print(user.id)
    sir=ServiceRequests.objects.filter(user=user)
    context={
        'form': form,
        'sir':sir
        }
    
    return render(request, 'service_request_form.html', context)


from .models import ServiceRequests

def user_req(request):
    bot=BotProfile.objects.all()
    print(bot)
    service_requests = ServiceRequests.objects.all()
    return render(request, 'user_req.html', {'service_requests': service_requests,'bot':bot})



from django.http import JsonResponse
from django.shortcuts import render
from .models import BotProfile, ServiceRequest

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ServiceRequests, BotProfile

def req_approve(request):
    if request.method == 'POST':
        botanist_id = request.POST.get('botanist')
        service_id = request.POST.get('service')
        user_id = request.POST.get('user')  # assuming user_id is passed in the request
        print(service_id)

        botanist = BotProfile.objects.get(id=botanist_id)
        service_requests = ServiceRequests.objects.get(id=service_id)
        service_requests.bot_profile = botanist
        service_requests.status = 'pending'
        service_requests.save()

        # Fetch the associated user details
        user_details = {
            'username': service_requests.user.username,
            'email': service_requests.user.email,
            # add more user details as needed
        }

        return JsonResponse({'message': 'Service request approved successfully.', 'user_details': user_details})

    # If the request method is GET, render the approval form
    botanists = BotProfile.objects.all()
    service_requests = ServiceRequests.objects.all()
    return render(request, 'req_approve.html', {'bot': botanists, 'service_requests': service_requests})



from .models import ServiceRequests

def service_requests_view(request):
    # Fetch all service requests
    bot=BotProfile.objects.get(user=request.user)
    print(bot)
    service_requests = ServiceRequests.objects.filter(bot_profile_id=bot.id)
    print(service_requests)
    print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    return render(request, 'service_requests.html', {'service_requests': service_requests})


# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .models import ServiceRequests

def approve_request(request, request_id):
    service_request = get_object_or_404(ServiceRequests, id=request_id)
    # Logic to send an approval message to the user
    service_request.status ='confirm'
    service_request.save()
    messages.success(request, 'Request approved. Message sent to the user.')
    return redirect('service_requests')

def reject_request(request, request_id):
    service_request = get_object_or_404(ServiceRequests, id=request_id)
    service_request.status ='reject'
    service_request.save()
    messages.warning(request, 'Request rejected. Message sent to the user.')
    return redirect('service_requests')

def agri(request):
    return render(request,'agri.html')

#work

# from django.shortcuts import render, redirect
# from .forms import BotanistWorksForm
# from .models import BotanistWorks

# def add_work(request):
#     if request.method == 'POST':
#         form = BotanistWorksForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('work_display')  # Redirect to a success page after form submission
#     else:
#         form = BotanistWorksForm()
#     return render(request, 'add_work.html', {'form': form})

# def work_display(request):
#     return render(request, 'work_display.html')

from django.shortcuts import render, redirect
from .forms import BotanistWorForm

def add_botanist_work(request):
    if request.method == 'POST':
        form = BotanistWorForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.botanist = request.user.botprofile  # Assuming user is authenticated and has a botprofile
            work.save()
            return redirect('consult')  # Redirect to a success page after successful form submission
    else:
        form = BotanistWorForm()
    return render(request, 'add_botanist_work.html', {'form': form})




from django.shortcuts import render
from .models import BotanistWorkk

def display_botanist_work(request):
    botanist_works = BotanistWorkk.objects.all()
    return render(request, 'display_botanist_work.html', {'botanist_works': botanist_works})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import BotanistWorkk
from .forms import BotanistWorForm

def botanist_work_list(request):
    botanist_works = BotanistWorkk.objects.all()
    return render(request, 'botanist_work_list.html', {'botanist_works': botanist_works})

from django.shortcuts import render, redirect, get_object_or_404
from .models import BotanistWorkk
from .forms import BotanistWorForm

def edit_work(request, pk):
    work = get_object_or_404(BotanistWorkk, pk=pk)
    if request.method == 'POST':
        form = BotanistWorForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            return redirect('botanist_work_list')  # Redirect to the list of works
    else:
        form = BotanistWorForm(instance=work)
    return render(request, 'edit_work.html', {'form': form})

def delete_work(request, pk):
    work = get_object_or_404(BotanistWorkk, pk=pk)
    if request.method == 'POST':
        work.delete()
        return redirect('botanist_work_list')  # Redirect to the list of works
    # If the request method is not POST (e.g., GET), simply redirect to the list of works
    return redirect('botanist_work_list')


# views.py

from django.shortcuts import render, redirect
from .models import CustomerPhoto
from .forms import CustomerPhotoForm

def upload_photo(request):
    if request.method == 'POST':
        form = CustomerPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to success page or wherever you want
    else:
        form = CustomerPhotoForm()
    user= request.user
    return render(request, 'upload_photo.html', {'form': form,'user':user})

from .models import CustomerPhoto

def customer_photos_view(request):
    photos = CustomerPhoto.objects.all()
    return render(request, 'customer_photos.html', {'photos': photos})


def subsidy(request):
    return render(request,'subsidy.html')

from django.shortcuts import render, redirect
from .forms import ItemForm

def subsidy_list(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('horticulture')  # Redirect to the subsidy list view after saving the item
        # If the form is not valid, render the create_item.html template with the form containing validation errors

    form = ItemForm()
    return render(request, 'subsidy_list.html', {'form': form})

from django.shortcuts import render
from .models import Itemss

def items(request):
    # Fetch items from the Itemss model
    items = Itemss.objects.all()
    return render(request, 'items.html', {'items': items})



from django.contrib.auth.decorators import login_required

@login_required
def order_status(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_status.html', {'orders': orders})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

def cancel_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        if order.payment_status:
            order.cancelled = True
            order.save()
            messages.success(request, 'Order cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel unpaid orders.')
    return redirect('order_status')  # Redirect to the order status page



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

def order_cancellation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        # Assuming you handle the cancellation logic here
        order.cancel()  # You may have a method like cancel() in your Order model
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})



from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Order

def order_status(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_status.html', {'orders': orders})


from django.shortcuts import render
from .models import Itemss

def sub_sett(request):
    items = Itemss.objects.all()
    return render(request, 'sub_sett.html', {'items': items})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Itemss
from .forms import ItemForm  # Assuming you have an ItemForm defined in forms.py

def edit_item(request, item_id):
    item = get_object_or_404(Itemss, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sub_sett')  # Redirect to the item list page
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Itemss

def delete_item(request, item_id):
    item = get_object_or_404(Itemss, pk=item_id)
    
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    
    return JsonResponse({'error': 'Invalid request'})


def receipt_view(request):
    
    return render(request, 'receipt.html')

def detect(request):
    
    return render(request, 'detect.html')

from django.shortcuts import render
from .models import Book

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})
