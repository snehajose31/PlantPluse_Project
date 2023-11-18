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
   





def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_authenticated:
                
                print(user)
                if user is not None:
                    klogin(request, user)
                    if user.role == User.Role.ADMIN:  # Assuming you have a 'role' field to distinguish between users and admins
                        # Log in the admin user
                        return redirect('/adminpanel/')  # Redirect to the admin panel URL
                    elif user.role == User.Role.CUSTOMER:  # Assuming you have a 'role' field to distinguish between users and admins
                        # Log in the admin user
                        return redirect('home')
                    elif user.role == User.Role.BOTANIST:  # Assuming you have a 'role' field to distinguish between users and admins
                        # Log in the admin user
                        return redirect('consult')
                    # else:
                    #     request.session["useremail"] = user.email
                    #     return redirect('/home')  # Redirect to the regular user's home page
                else:
                    messages.error(request, "Invalid credentials.")
                    return redirect('/login')
    
    return render(request, 'login.html')  # Render the login page



def about(request):
    return render(request,'about.html')

def home(request):
    user = request.user
    print(user) 
    return render(request,'home.html',{'user':user})

def contact(request):
    return render(request,'contact.html')


def profile(request):
    user=request.user
    try:
        userinfo=UserInfo.objects.filter(user=user)
        if request.method == 'POST':
            full_name = request.POST.get('fullname')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date-of-birth')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            user_info = UserInfo(user=request.user, contact_no=phone, place='', city='', district='', pincode='')
        user_info.save()
         
    except:
         userinfo=UserInfo()   
    
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


def view_cart(request):
    user=request.user
    user_id = user.id
    print(user_id)
    cart_items = AddToCart3.objects.filter(user=user_id, is_active=True)

    # Ensure the quantity is at least 1 and update the total price based on the quantity
    for item in cart_items:
        if item.product.stock < 1 or item.product.stock is None:
            item.product.stock = 1  # Set the minimum quantity to 1
        item.total_price = item.product.sale_price * item.product.stock # Update the total price based on the new quantity

    # Calculate order summary
    subtotal = sum(item.total_price for item in cart_items)
    shipping = 5  # Adjust this value as needed
    total = subtotal + shipping

    context = {
    'cart_items': cart_items,
    'subtotal': subtotal,
    'shipping': shipping,
    'total': total,
    'total_amount': total,  # Add the total amount to the context
}

    return render(request, 'view_cart.html', context)

def add_to_cart(request, id):
    # Retrieve the product based on its ID (you should have a Product model)
    product = Product2.objects.get(pk=id) 
    user=request.user
    email=user.email
    user = get_object_or_404(User, email=email)
    
        # Check if the user already has this product in their cart
    cart_item = AddToCart3(user=user, product=product)  # You can set the quantity as neede
    cart_item.save()
    print(cart_item)
    return redirect('view_cart') 

def flowering_plants(request):
    # Retrieve products under the "flowering plants" subcategory
    flowering_plants = Product2.objects.filter(category_id="1", subcategory_id='1')
    print(flowering_plants)  # Add this line for debugging

    return render(request, 'flowering_plants.html', {'products': flowering_plants})

def medicinal_plants(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    medicinal_plants = Product2.objects.filter(category="1", subcategory='2')
    print(medicinal_plants)
    
    return render(request, 'medicinal_plants.html', {'products': medicinal_plants})

def organic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    organic = Product2.objects.filter(category="2", subcategory='4')
    print(organic)
    
    return render(request, 'organic.html', {'products': organic})

def inorganic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    inorganic = Product2.objects.filter(category="2", subcategory='3')
    print(inorganic)
    
    return render(request, 'inorganic.html', {'products': inorganic})

def vegetable_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    vegetable_seed = Product2.objects.filter(category="3", subcategory='5')
    print(vegetable_seed)
    
    return render(request, 'vegetable_seed.html', {'products': vegetable_seed})

def flowering_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    flowering_seed = Product2.objects.filter(category="seed", subcategory='flowering seed')
    print(flowering_seed)
    
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



def remove_from_cart(request, item_id):
    item = get_object_or_404(AddToCart3, pk=item_id)

    if item.user == request.user:
        # Remove the item from the cart and the database
        item.delete()

    # Recalculate order summary after item removal
    cart_items = AddToCart3.objects.filter(user=request.user, is_active=True)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    shipping = 10  # Adjust this value as needed
    total = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'view_cart.html', context)



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




def wishlist(request):
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