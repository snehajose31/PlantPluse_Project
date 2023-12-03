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

def user_r(request):
    user_s = User.objects.all()  # Fetch all products
    return render(request, 'user.html', {'user_s': user_s})

def botanist_t(request):
    return render(request,'botanist.html')

def bot_t(request):
    return render(request,'bot.html')

def custome_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

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
def flowering_plants(request):
    flowering_plants = Product2.objects.filter(category_id="1", subcategory_id='1')
    return render(request, 'flowering_plants.html', {'products': flowering_plants})

# def flowering_plants(request):
#     # Retrieve products under the "flowering plants" subcategory
#     flowering_plants = Product2.objects.filter(category_id="1", subcategory_id='1')
#     print(flowering_plants)  # Add this line for debugging

#     return render(request, 'flowering_plants.html', {'products': flowering_plants})

def medicinal_plants(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    medicinal_plants = Product2.objects.filter(category="1", subcategory='2')
    return render(request, 'medicinal_plants.html', {'products': medicinal_plants})

def organic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    organic = Product2.objects.filter(category="2", subcategory='4')
    
    
    return render(request, 'organic.html', {'products': organic})

def inorganic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    inorganic = Product2.objects.filter(category="2", subcategory='3')
    
    
    return render(request, 'inorganic.html', {'products': inorganic})

def vegetable_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    vegetable_seed = Product2.objects.filter(category="3", subcategory='5')
    
    
    return render(request, 'vegetable_seed.html', {'products': vegetable_seed})

def flowering_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    flowering_seed = Product2.objects.filter(category="seed", subcategory='flowering seed')
    
    
    return render(request, 'floweringseed.html', {'products': flowering_seed})

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
 
 
 
def consult(request):
    return render(request,'consult.html')

# def book_appointment(request):
#     return render(request, 'book-appointment.html')

def botdetail(request):
    return render(request,'botdetail.html')

# views.py


from .models import Botanist, Appointment
from django.http import HttpResponse

def consultation_form(request):
    if request.method == 'POST':
        selected_date = request.POST.get('appointment-date')
        selected_time = request.POST.get('appointment-time')
        selected_botanist_id = request.POST.get('botanist')
        subject = request.POST.get('subject')

        # Validate the form data
        if selected_date and selected_time and selected_botanist_id and subject:
            try:
                selected_botanist = Botanist.objects.get(pk=selected_botanist_id)

                # Save the appointment to the database
                appointment = Appointment(
                    appointment_date=selected_date,
                    appointment_time=selected_time,
                    botanist=selected_botanist,
                    subject=subject
                )
                appointment.save()

                # Redirect to the botanist.html page
                return redirect('botanist_page')  # Replace 'botanist_page' with the actual name or URL pattern of your botanist.html page
            except Botanist.DoesNotExist:
                # Handle the case where the selected botanist does not exist
                return HttpResponse("Invalid botanist selected.")
        else:
            # Handle the case where form data is incomplete
            return HttpResponse("Please fill out all fields before scheduling the appointment.")
    else:
        # Retrieve botanists from the database to populate the form
        botanists = Botanist.objects.all()

        context = {
            'botanists': botanists,
        }

        return render(request, 'book-appointment.html', context)

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


def bill_invoice(request):
    # Fetch the latest order for the logged-in user (or implement your logic)
    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'billinvoice.html', {'order': order})


def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'order_history.html', {'orders': orders})

