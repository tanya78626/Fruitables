from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import *
from django.http import HttpResponse

# Create your views here.
def register(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            password = request.POST.get('password')
            city = request.POST.get('city')

            Register.objects.create(
                name=name,
                email=email,
                contact=contact,
                password=password,
                city=city
            )

            messages.success(request, "Register successfully")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')

def login(request):

    if request.method=="POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.filter(email=email, password=password).first()
            if user:
                messages.success(request,"Login Successfull!")
                return redirect('index')
            else:
                messages.error(request,"invalid email or password")
                return render (request, "login.html")
            
        except Exception as e:
            messages.error(request, "Login failed:")
            return render(request, "login.html")
        
    return render(request,'login.html')

def error(request):
    return render(request, '404.html')

def cart(request):
    # Get all cart items
    items = Cart.objects.all()
 
    # Calculate subtotal for each item
    for item in items:
        item.subtotal = float(item.product.price) * item.quantity
 
    # Calculate total cart price
    total_price = sum(item.subtotal for item in items)
 
    # Optional: set flat shipping
    shipping = 3.00
    total_with_shipping = total_price + shipping
 
    return render(request, "cart.html", {
        "items": items,
        "total_price": total_price,
        "shipping": shipping,
        "total_with_shipping": total_with_shipping
    })    

def checkout(request):
    cart_items = Cart.objects.select_related('product')

    subtotal = 0
    for item in cart_items:
        price = float(item.product.price)
        item.total_price = price * item.quantity
        subtotal += item.total_price

    shipping = 3.00 if subtotal > 0 else 0
    total = subtotal + shipping

    if request.method == 'POST':
        # store data temporarily in session
        request.session['checkout_data'] = {
            'first_name': request.POST.get('firstname', ''),
            'last_name': request.POST.get('lastname', ''),
            'companyname': request.POST.get('companyname', ''),
            'address': request.POST.get('address', ''),
            'city': request.POST.get('city', ''),
            'country': request.POST.get('country', ''),
            'pincode': request.POST.get('pincode', ''),
            'mobile': request.POST.get('mobile', ''),
            'email': request.POST.get('email', ''),
            'create_account': True if request.POST.get('create_account') else False,
            'ship_to_different_address': True if request.POST.get('ship_to_different_address') else False,
            'order_notes': request.POST.get('notes', '')
        }

        return redirect('place_order')

    return render(request, 'checkout.html', {
        'items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })

def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')

def shop_detail(request):
    return render(request, 'shop-detail.html')

def shop(request):
    category = request.GET.get('category')  # fruit / vegetable
 
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
 
    return render(request, "shop.html", {
        "products": products,
        "selected_category": category
    })
 
 

def testimonial(request):
    return render(request, 'testimonial.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
 
    cart_item, created = Cart.objects.get_or_create(
        product=product
    )
 
    if not created:
        cart_item.quantity += 1
 
    cart_item.save()
    return redirect('cart')

def plus_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')
 
 
# Decrease Quantity
def minus_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, product=product)
 
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
 
    return redirect('cart')
 
 
# Remove Item
def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.filter(product=product).delete()
    return redirect('cart')


import razorpay
from django.conf import settings
 
def place_order(request):
    cart_items = Cart.objects.select_related('product')

    subtotal = 0
    for item in cart_items:
        subtotal += float(item.product.price) * item.quantity

    shipping = 3.00 if subtotal > 0 else 0
    total = subtotal + shipping

    # convert to paise
    amount = int(total * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
    "items": cart_items,
    "subtotal": subtotal,
    "shipping": shipping,
    "total": total,
    "razorpay_key": settings.RAZORPAY_KEY_ID,
    "amount": amount,
    "order_id": payment['id'],
}

    return render(request, "payment.html", context)

def search_item(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('shop')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(descriptions__icontains=query)   # ✅ CORRECT FIELD
    )

    return render(request, 'shop.html', {
        'products': products,
        'query': query
    })

def confirm_order(request):
    return render(request, 'confirm_order.html')

def payment(request):
    return render(request,'payment.html')
