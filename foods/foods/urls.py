# foods/urls.py

from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    # for navigation-bar 
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    
    # for admin 
    path('admin/', admin.site.urls),
    
    # for register and login purpose
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_view, name='register'),
    
    # for seperate categories 
    path('food/category/starter/', views.starter, name='starter'),
    path('food/category/mainCourse/', views.mainCourse, name='mainCourse'),
    path('food/category/dessert/', views.dessert, name='dessert'),
    path('cart/add/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
