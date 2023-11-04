from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login as klogin,logout
from django.contrib import messages
from . models import User
from django.template import RequestContext
# from django.http import HttpResponse
from . models import Product
from . models import User
from django.shortcuts import get_object_or_404


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
            product_image=product_image
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
    product = get_object_or_404(Product, id=product_id)

    # Render the product details template with the product data
    return render(request, 'details.html', {'product': product})

def edit_product(request, product_id):
    # Retrieve the product using get_object_or_404 to handle cases where the product doesn't exist
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Handle form submission and update the product
        # You can access form data using request.POST and request.FILES
        # Perform validation and update the product data in the database

        # Example:
        product.product_name = request.POST['product-name']
        # product.category = request.POST['category-name']
        # product.subcategory = request.POST['subcategory-name']
      
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.discount = request.POST['discount']
        product.sale_price = request.POST['sale-price']
        
        # Save the updated product
        product.save()

        # Redirect to a product detail page or a success page
        #return HttpResponseRedirect('/product_detail/{0}/'.format(product.product_id))
       # return HttpResponseRedirect('adminpanel')

    # If the request method is GET, render the edit product form
    return render(request, 'editproduct.html', {'product': product})