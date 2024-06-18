from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Dessert, MainCourse, Starter, Cart, CartItem, User, UserAuth
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.db.models import Q

# for registeration purpose 
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=name, email=email, password=password)
        user_auth = UserAuth.objects.create(email=email)
        user_auth.set_password(password)

        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user_auth = UserAuth.objects.get(email=email)
            if user_auth.check_password(password):
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error_message = "Authentication failed."
            else:
                error_message = "Invalid password. Please try again."
        except UserAuth.DoesNotExist:
            error_message = "Invalid email. Please try again."
        
        return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    form_data = None
    if request.method == "POST":
        form_data = {
            'name': request.POST.get('name'),
            'age': request.POST.get('age'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'zipcode': request.POST.get('zipcode'),
            'feedback': request.POST.get('feedback'),
        }
    return render(request, 'contact.html', {'form_data': form_data})

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        desserts = Dessert.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(rating__icontains=query) |
            Q(product_id__icontains=query) |
            Q(brand_name__icontains=query)
        )
        main_courses = MainCourse.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(rating__icontains=query) |
            Q(product_id__icontains=query) |
            Q(brand_name__icontains=query)
        )
        starters = Starter.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(rating__icontains=query) |
            Q(product_id__icontains=query) |
            Q(brand_name__icontains=query)
        )

        # Retrieve cart items
        cart_items = []
        if 'cart_id' in request.session:
            cart = Cart.objects.filter(session_id=request.session['cart_id']).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)

        # Filter results to include only items in cart
        for dessert in desserts:
            if any(cart_item.product_id == dessert.id and cart_item.product_type == 'dessert' for cart_item in cart_items):
                results.append(dessert)

        for main_course in main_courses:
            if any(cart_item.product_id == main_course.id and cart_item.product_type == 'main_course' for cart_item in cart_items):
                results.append(main_course)

        for starter in starters:
            if any(cart_item.product_id == starter.id and cart_item.product_type == 'starter' for cart_item in cart_items):
                results.append(starter)

    return render(request, 'search_results.html', {'query': query, 'results': results})

def dessert(request):
    foods = Dessert.objects.all()
    return render(request, 'dessert.html', {'foods': foods})

def mainCourse(request):
    foods = MainCourse.objects.all()
    return render(request, 'main_course.html', {'foods': foods})

def starter(request):
    foods = Starter.objects.all()
    return render(request, 'starter.html', {'foods': foods})

def add_to_cart(request, product_type, product_id):
    if 'cart_id' not in request.session:
        request.session['cart_id'] = get_random_string(32)
    
    cart, created = Cart.objects.get_or_create(session_id=request.session['cart_id'])
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_type=product_type,
        product_id=product_id
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return JsonResponse({'status': 'success'})

def view_cart(request):
    if 'cart_id' not in request.session:
        return render(request, 'cart.html', {'cart_items': [], 'total_bill': 0, 'discount': 0, 'discounted_total': 0, 'cgst': 0, 'sgst': 0, 'final_total': 0})
    
    cart = get_object_or_404(Cart, session_id=request.session['cart_id'])
    cart_items = CartItem.objects.filter(cart=cart)
    
    products = []
    total_bill = Decimal('0.00')
    discount = Decimal('0.00')
    for item in cart_items:
        product = item.get_product()
        if product:
            total_price = product.price * item.quantity
            products.append({
                'id': item.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': item.quantity,
                'total_price': total_price,
            })
            total_bill += total_price
    
    if total_bill > Decimal('500.00'):
        discount = Decimal('100.00')
    
    discounted_total = total_bill - discount
    cgst = discounted_total * Decimal('0.025')
    sgst = discounted_total * Decimal('0.025')
    final_total = discounted_total + cgst + sgst
    
    return render(request, 'cart.html', {
        'cart_items': products,
        'total_bill': total_bill,
        'discount': discount,
        'discounted_total': discounted_total,
        'cgst': cgst,
        'sgst': sgst,
        'final_total': final_total
    })

def update_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            return JsonResponse({'status': 'removed'})
    cart_item.save()
    
    return JsonResponse({'status': 'success', 'quantity': cart_item.quantity})
