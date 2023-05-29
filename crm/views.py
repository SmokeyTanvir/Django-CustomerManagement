from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from django.urls import reverse
from .filters import OrderFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='login')
@admin_only
def index(request):
    ordersCount = Order.objects.count()
    ordersDelivered = Order.objects.filter(status='Delivered').count()
    ordersPending = Order.objects.filter(status='Pending').count()
    context = {
        'customers' : Customer.objects.all(),
        'ordersCount' : ordersCount,
        'ordersDelivered' : ordersDelivered,
        'ordersPending' : ordersPending,
        'orders': Order.objects.all()
    }
    return render(request, 'crm/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, customerID):
    customer = Customer.objects.get(id=customerID)
    all_orders = customer.order_set.all()
    total_orders = all_orders.count()

    myfilter = OrderFilter(request.GET, queryset=all_orders)
    all_orders = myfilter.qs

    context = {
        'customer' : customer,
        'total_orders' : total_orders,
        'orders' : all_orders,
        'myfilter' : myfilter
    }
    return render(request, 'crm/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products =  Product.objects.all()
    return render(request, 'crm/products.html', {
        'products': products
    })

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save() 
            return redirect(reverse("customer", args=[customer.id]))

    context = {
        'formset' : formset
    }
    return render(request, 'crm/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, orderID):
    print(f"order id : {orderID}")
    order = Order.objects.get(id=orderID)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(reverse("index"))

    context = {'form': form}

    return render(request, 'crm/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, orderID):
    order = Order.objects.get(id=orderID)
    
    if request.method == 'POST':
        order.delete()
        return redirect(reverse("index"))
    
    context = {
        'item' : order
    }

    return render(request, 'crm/delete.html', context)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST': 
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            Customer.objects.create(user=user)
            user.groups.add(group)

            return redirect('login')
            
    context = {
        'form' : form,
    }
    return render(request, 'crm/register.html', context)

@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Invalid Username or Password')  
    
    context = {

    }
    return render(request, 'crm/login.html', context)


def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out.")
        return redirect("login")
    else:
        messages.warning(request, 'You are not logged in.')
        return redirect('login')
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    ordersCount = orders.count()
    ordersDelivered = orders.filter(status='Delivered').count()
    ordersPending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'ordersCount': ordersCount,
        'ordersDelivered': ordersDelivered,
        'ordersPending': ordersPending
    }

    return render(request, 'crm/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer

    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form': form
    }
    return render(request, 'crm/account_settings.html', context)