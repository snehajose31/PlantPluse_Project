from django.contrib import admin
from. import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import change_password
from .views import upload_video
# from .views import display_videos
from .views import chatgpt, generate_response
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
    
    path('checkot/',views.checkout, name='checkot'),
    
    path('profile/', views.profile1,name='profile'),
    path('horti/', views.horti,name='horti'),
    
    
    path('log/', views.change_password,name='log'),
    path('change_password/', change_password, name='change_password'),
    
    
    path('addproduct/',views.add_product,name="addproduct"),
    path('viewproduct/',views.view_product,name="viewproduct"),
    path('plants/',views.product_grid,name="plants"),
    path('user/',views.user_r,name="user"),
    path('botanist/',views.botanist_t,name="botanist"),
    path('hort/',views.hort,name="hort"),
    path('bot/',views.bot_t,name="bot"),
    path('book/',views.book,name="book"),
    
    path('logout/',views.custome_logout,name="logout"),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    # path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('regibot/',views.regbot,name="regibot"),
    path('reghorti/',views.reghorti,name="reghorti"),
    path('consult/',views.consult,name="consult"),
    
    path('horticulture/',views.horticulture,name="horticulture"),
    path('book-appointment/<int:id>/',views.consultation_form, name='book-appointment'),
    path('botdetail/',views.botdetail,name="botdetail"),
    # path('consultation/',views.consultation_form, name='consultation_form'),
    path('search_user/',views.search_user, name='search_user'),
    path('work/',views.works, name='work'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('deactivate-user/<int:user_id>/',views.deactivate_user, name='deactivate_user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wish/',views.wishs, name='wish'),

    path('profile/',views.pf, name='profile'),
    path('delete_from_wishlist/<int:id>/',views.delete_from_wishlist, name='delete_from_wishlist'),
    
    
    path('plants/flowering plant/', views.flowering_plants, name='flowering_plants'),
    path('subcategory/flowering-plants/', views.flowering_plants, name='flowering_plants'),
    path('subcategory/medicinal-plants/', views.medicinal_plants, name='medicinal_plants'),
    path('subcategory/organic/', views.organic, name='organic'),
    path('subcategory/inorganic/', views.inorganic, name='inorganic'),
    path('sucategory/seed/',views.vegetable_seed,name='vegetable_seed'),
    path('sucategory/seed/',views.flowering_seed,name='flowering_seed'),
    # path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search_products, name='search_products'),
    
    path('user_profile/',views.user_profile, name='user_profile'),
    path('save_profile/',views.save_profile, name='save_profile'),
    path('save_profile1/',views.save_profile1, name='save_profile1'),
    
    path('user_profile/',views.user_profile,name='user_profile'),
    
    
    path('order_complete/', views.order_complete, name='order_complete'),
    path('billinvoice/', views.bill_invoice, name='bill_invoice'),
    path('order_history/', views.order_history, name='order_history'),
    path('search/',views.search_prod, name='search_prod'),
    
    #appointment
    path('appoint/', views.scheduling, name='scheduling'),
    path('appoint/', views.scheduling, name='appoint'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
     path('botanist_list/', views.botanist_list, name='botanist_list'),
    
    

    
    
    path('add-to-cart/<int:id>/',views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/',views.remove_from_cart, name='remove-from-cart'),
    path('view_cart/',views.view_cart, name='view_cart'),
    path('increase-cart-item/<int:id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/',views.fetch_cart_count, name='fetch-cart-count'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('create-order/',views.create_order, name='create-order'),
    path('handle-payment/',views.handle_payment, name='handle-payment'),
    # path('checkot/',views.checkout, name='checkot'),
    
    
    #time_slot
    path('get_time_slots/<str:selected_date>/',views.get_time_slots, name='get_time_slots'),
    
    
    path('bot_profile/', views.bot_profile, name='bot_profile'),
    path('save_profile1/', views.save_profile1, name='save_profile1'),
    path('user_profil/',views.user_profil, name='user_profil'),
    
    #video
    path('upload_video/', upload_video, name='upload_video'),
    path('display_videos/',views.display_videos, name='display_videos'),
    
    #chatgpt nrs

    path('chatgpt/', chatgpt, name='chatgpt'),
    path('generate-response/', generate_response, name='generate_response'),
    path('user-list/', views.user_list, name='user_list'),  # Use 'user_list' instead of 'user-list'
    path('delete-user/<str:username>/', views.delete_user, name='delete_user'),
    
    path('videos/', views.video_list, name='video_list'),
    path('videos/delete/<int:video_id>/',views.delete_video, name='delete_video'),
    path('videos/', views.video_list, name='videos'),

 
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
