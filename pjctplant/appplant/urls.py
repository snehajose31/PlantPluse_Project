from django.contrib import admin
from. import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns = [
   
    #path('index/',views.index,name="index")
    path('',views.index,name="index"),
    path('registration/', views.registration,name='registration'),
    path('login/', views.login,name='login'),
    path('about/', views.about,name='about'),
    path('home/', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('contact/',views.contact,name="contact"),
    path('accounts/login/', views.login, name='login'),
    path('adminpanel/',views.adminpanel,name="adminpanel"),
    
    path('addproduct/',views.add_product,name="addproduct"),
    path('viewproduct/',views.view_product,name="viewproduct"),
    path('plants/',views.product_grid,name="plants"),
    path('user/',views.user_r,name="user"),
    path('botanist/',views.botanist_t,name="botanist"),
    path('bot/',views.bot_t,name="bot"),
    path('logout/',views.custome_logout,name="logout"),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('regibot/',views.regbot,name="regibot"),
    path('consult/',views.consult,name="consult"),
    path('book-appointment/',views.consultation_form, name='book-appointment'),
    path('botdetail/',views.botdetail,name="botdetail"),
    # path('consultation/',views.consultation_form, name='consultation_form'),
    path('search_user/',views.search_user, name='search_user'),
    path('work/',views.works, name='work'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('deactivate-user/<int:user_id>/',views.deactivate_user, name='deactivate_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    
    
    
    path('plants/flowering plant/', views.flowering_plants, name='flowering_plants'),
    path('subcategory/flowering-plants/', views.flowering_plants, name='flowering_plants'),
    path('subcategory/medicinal-plants/', views.medicinal_plants, name='medicinal_plants'),
    path('subcategory/organic/', views.organic, name='organic'),
    path('subcategory/inorganic/', views.inorganic, name='inorganic'),
    path('sucategory/seed/',views.vegetable_seed,name='vegetable_seed'),
    path('sucategory/seed/',views.flowering_seed,name='flowering_seed'),
    # path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search_products, name='search_products'),
 
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
