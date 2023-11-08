from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login as klogin,logout
from django.contrib import messages
from . models import User
from django.template import RequestContext
# from django.http import HttpResponse
from . models import Product
from . models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user


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
   



# def login(request):
#     # if 'email' in request.session:
#     #     return redirect('/')
    
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]

#         if username and password:
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                     print(f"User: {user.username}, Role: {user.role}")
#                     if user.role == User.Role.CUSTOMER:
#                         request.session["email"] = user.email
#                         return redirect('/home')
#                     else:
#                         messages.error(request, "Invalid credentials.")
#                         return redirect('/login')

#             else:
#                 messages.error(request, "Invalid credentials.")
#                 return redirect('/login')
#         else:
#             messages.error(request, "Please fill out all fields.")
#             return redirect('/login')
    
#     return render(request, 'login.html')





def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = authenticate(request, email=username, password=password)
            if user.is_authenticated:

                if user is not None:
                    if user.role == User.Role.ADMIN:  # Assuming you have a 'role' field to distinguish between users and admins
                        # Log in the admin user
                        return redirect('/adminpanel/')  # Redirect to the admin panel URL
                    else:
                        request.session["useremail"] = user.email
                        return redirect('/home')  # Redirect to the regular user's home page
                else:
                    messages.error(request, "Invalid credentials.")
                    return redirect('/login')
        else:
            messages.error(request, "Please fill out all fields.")
            return redirect('/login')

    return render(request, 'login.html')


    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
        
    #     if user is not None:
    #         login(request, user)
    #         request.session['username'] = user.username
    #         return redirect('index')
    # else:  
    #     return render(request, 'login.html', {'error_message': 'Invalid credentials!!'})

    # return render(request, 'login.html')


def about(request):
    return render(request,'about.html')

def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')

def profile(request):
    return render(request,'profile.html')

# def your_view(request):
#     # Your view logic here
#     return render(request, 'your_template.html', context_instance=RequestContext(request))

def adminpanel(request):
    return render(request,'adminpanel.html')


# def add_product(request):
#     if request.method == 'POST':
#         # Retrieve the form data submitted by the user
#         category_name = request.POST.get('category-name')
#         subcategory_name = request.POST.get('subcategory-name')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')
#         sale_price = request.POST.get('sale-price')
#         status = request.POST.get('status')
#         # Handle the product image as needed, it can be accessed through request.FILES['product-image']

#         # Process the data as needed, for example, saving it to a database
#         # You can create a Product model and save the data like this:
#         # product = Product(category=category_name, subcategory=subcategory_name, quantity=quantity, description=description, price=price, discount=discount, sale_price=sale_price, status=status)
#         # product.save()

#         # Redirect to a success page or perform any other action
#         return HttpResponse('Product added successfully!')
#     else:
#         # Render the HTML form for GET requests
#         return render(request, 'add_product.html')
def add_product(request):
    if request.method == 'POST':
        # Handle the form submission
        product_id = request.POST.get('product-id')
        product_name = request.POST.get('product-name')
        category = request.POST.get('category-name')
        subcategory = request.POST.get('subcategory-name')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')  # Retrieve as a string
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        price = float(price)

        # Convert discount to a float
        discount = float(discount)

        
        

        # Calculate sale_price
        sale_price = price - (price * (discount / 100))

        # Create a new Product object and save it to the database
        product = Product(
            product_id=product_id,
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            quantity=quantity,
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,  # Assign the calculated sale price
            status=status,
            product_image=product_image,
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('viewproduct')

    return render(request, 'addproduct.html')




def view_product(request):
    # Assuming you have a queryset of products (e.g., Product.objects.all())
    products = Product.objects.all()  # Modify this to fetch the products
    return render(request, 'viewproduct.html', {'products': products})

def product_grid(request):
    products = Product.objects.all()  # Fetch all products
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


def delete_product(request, product_id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return redirect('viewproduct')
        except Product.DoesNotExist:
            pass
    return redirect('viewproduct')  # Redirect back to the product list view

def product_details(request, product_id):
    # Retrieve the product details from the database
    product = get_object_or_404(Product, pk=product_id)

    # Render the product details template with the product data
    return render(request, 'details.html', {'product': product})



# def edit_product(request, product_id):
#     # Retrieve the product using get_object_or_404 to handle cases where the product doesn't exist
#     product = get_object_or_404(Product, pk=product_id)

#     if request.method == 'POST':
#         try:
#             # Update the product with the form data
#             product.product_name = request.POST.get('product-name', product.product_name)
#             product.category = request.POST.get('category-name', product.category)
#             product.subcategory = request.POST.get('subcategory-name', product.subcategory)
#             product.description = request.POST.get('description', product.description)
#             product.price = request.POST.get('price', product.price)
#             product.discount = request.POST.get('discount', product.discount)
#             product.sale_price = request.POST.get('sale-price', product.sale_price)

#             # Save the updated product
#             product.save()

#             # Redirect to a view or success page
#             return redirect('viewproduct')  # Replace 'viewproduct' with the actual URL name

#         except Exception as e:
#             # Handle exceptions, such as validation errors
#             # You can return an error message or render the form with error details
#             return render(request, 'editproduct.html', {'product': product, 'error_message': str(e)})

#     # If the request method is GET, render the edit product form
#     return render(request, 'editproduct.html', {'product': product})
        

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product  # Import your Product model



def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        try:
            product_name = request.POST.get('product-name')
            category = request.POST.get('category-name')
            subcategory = request.POST.get('subcategory-name')
            quantity = request.POST.get('quantity')
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
            product = Product(
                product_id=product_id,
                product_name=product_name,
                category=category,
                subcategory=subcategory,
                quantity=quantity,
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
    email=request.session["useremail"]
    user = get_object_or_404(User, email=email)
    user_id = user.id
    print(user_id)
    cart_items = AddToCart.objects.filter(user=user_id, is_active=True)

    # Calculate order summary
    # subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    # shipping = -15680 # Adjust this value as needed
    # total = subtotal + shipping
    
    context = {
        'cart_items': cart_items,
        # 'subtotal': subtotal,
        # 'shipping': shipping,
        # 'total': total,
    }
    return render(request, 'view_cart.html', context)

def add_to_cart(request, product_id):
    # Retrieve the product based on its ID (you should have a Product model)
    product = Product.objects.get(pk=product_id) 
    email=request.session["useremail"]
    user = get_object_or_404(User, email=email)
    
        # Check if the user already has this product in their cart
    cart_item = AddToCart(user=user, product=product, quantity=product_id)  # You can set the quantity as neede
    cart_item.save()
    print(cart_item)
    return redirect('view_cart') 

def flowering_plants(request):
    # Retrieve products under the "flowering plants" subcategory
    flowering_plants = Product.objects.filter(category="plant", subcategory='flowering plant')
    print(flowering_plants)  # Add this line for debugging

    return render(request, 'flowering_plants.html', {'products': flowering_plants})


def medicinal_plants(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    medicinal_plants = Product.objects.filter(category="plant", subcategory='Medicinal plant')
    print(medicinal_plants)
    
    return render(request, 'medicinal_plants.html', {'products': medicinal_plants})

def organic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    organic = Product.objects.filter(category="fertilizer", subcategory='organic')
    print(organic)
    
    return render(request, 'organic.html', {'products': organic})

def inorganic(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    inorganic = Product.objects.filter(category="fertilizer", subcategory='inorganic')
    print(inorganic)
    
    return render(request, 'inorganic.html', {'products': inorganic})

def vegetable_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    vegetable_seed = Product.objects.filter(category="seed", subcategory='vegetable seed')
    print(vegetable_seed)
    
    return render(request, 'vegetable_seed.html', {'products': vegetable_seed})

def flowering_seed(request):
    # Retrieve all products that belong to the "Medicinal Plants" subcategory
    flowering_seed = Product.objects.filter(category="seed", subcategory='flowering seed')
    print(flowering_seed)
    
    return render(request, 'flowering_seed.html', {'products': flowering_seed})

def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = Product1.objects.get(id=id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if created:
            # The item was added to the wishlist
            messages.success(request, f'{product.product_name} has been added to your wishlist.')
        else:
            # The item is already in the wishlist
            messages.warning(request, f'{product.product_name} is already in your wishlist.')
    return redirect('wishlist')


def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated