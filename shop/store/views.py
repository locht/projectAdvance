from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.models import User
from store.forms import RegistrationForm, EditProfileForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems':cartItems,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        customer, order = guestOrder(request, data)

    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)


def larmes(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems':cartItems,
    }
    return render(request, 'store/larmes.html', context)

def casio(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems':cartItems,
    }
    return render(request, 'store/casio.html', context)

def citizen(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems':cartItems,
    }
    return render(request, 'store/citizen.html', context)

def daumier(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products' : products,
        'cartItems':cartItems,
    }
    return render(request, 'store/daumier.html', context)

def done(request):
    return render(request, 'store/done.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/register-done/") #thêm return ở đây thì k cần thêm href {% url %} cho action bên template (ngược lại - có url thì k cần dòng return)
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def view_profile(request):
    args = {'user':request.user}
    return render(request, 'store/profile.html', args)

def register_done(request):
    return render(request, 'store/register-done.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profile/")
    else:
        form = LoginForm()
    context = {
        'form':form
    }
    return render(request, 'store/login.html', context)