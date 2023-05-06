from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

from django.contrib.auth import login as auth_login
from .forms import LoginForm

from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# ------------------------------
from django.contrib.auth.models import User
from app.models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
# ------------------------------

# def home(request):
#  return render(request, 'app/home.html')

def search(request):
      data=Product.objects.all()
      product=request.GET.get('search')
      if product!=None:
        data=Product.objects.filter(title__icontains=product)
      return render(request,'app/search.html',{'data':data})

def get_items_count_in_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        for b in cart:
            totalitem += b.quantity
    return totalitem


class ProductView(View):
    def get(self, request):
        totalitem = get_items_count_in_cart(request)
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        # if request.user.is_authenticated:
        #     totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'totalitem': totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

# Class based views


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = get_items_count_in_cart(request)
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    # foreign key hai to product instance ka jarurat hoga
    product = Product.objects.get(id=product_id)
    #  print(product_id) debug
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    totalitem = get_items_count_in_cart(request)
    if request.user.is_authenticated:
        # totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 45.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # get se ak object milta hai
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        tempamount = 0.0
        shipping_amount = 45.0
        # cart ka user login ka user match hona chahiye
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount+shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # get se ak object milta hai
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        tempamount = 0.0
        shipping_amount = 45.0
        # cart ka user login ka user match hona chahiye
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount+shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # get se ak object milta hai
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        c.delete()
        amount = 0.0
        tempamount = 0.0
        shipping_amount = 45.0
        # cart ka user login ka user match hona chahiye
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount

        data = {
            #  amount jaise calculate ho raha hai waise hi calculate hoga
            'amount': amount,
            'total_amount': amount+shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    return render(request, 'app/profile.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    totalitem = get_items_count_in_cart(request)
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Iphone' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=45000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=45000)

    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})

def laptop(request, data=None):
    totalitem = get_items_count_in_cart(request)
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Hp' or data == 'Apple':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(
            category='M').filter(discounted_price__lt=45000)
    elif data == 'above':
        laptop = Product.objects.filter(
            category='M').filter(discounted_price__gt=45000)
    return render(request, 'app/laptop.html', {'laptop': laptop, 'totalitem': totalitem})

# Loginview ka yaha koi kam nahi hai kyoki django me bydefault-->LoginView hota hai-->auth_views me

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

# ------------------------------------------login up


class CustomerRegistrationView(View):
    # -------------------------------
    # --------------------------------
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = get_items_count_in_cart(request)
        return render(request, 'app/customerregistration.html', {'form': form, 'totalitem': totalitem})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        totalitem = get_items_count_in_cart(request)
        if form.is_valid():
            # message ko bhejne se kuchh nahi hoga usko dikhana padega
            # dikhayenge customerregistration.html me dikhayenge form tag ke andar me
            messages.success(
                request, 'Congturatulations!! Registered Successfully')
            form.save()
            # messages.success(request,'Congturatulations!! Registered Successfully')
        return render(request, 'app/customerregistration.html', {'form': form, 'totalitem': totalitem})


# ----------------------------------------------
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(
                request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')

        login(request, user)
        return redirect('/')

    return render(request, 'app/login.html')


def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'app/register.html')


def success(request):
    return render(request, 'app/success.html')


def token_send(request):
    return render(request, 'app/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'app/error.html')

# https://emartshop.site/
def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account https://emartshop.site/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    ret = send_mail(subject, message, email_from, recipient_list)

# -----------------------------------------------------


# class based view ke liye (method decorator)  for login required
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = get_items_count_in_cart(request)
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
    # for active Submit button write Post method

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        totalitem = get_items_count_in_cart(request)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    totalitem = get_items_count_in_cart(request)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 45.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            print(amount)
        total_amount = amount+shipping_amount
        print(total_amount)
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'amount': amount, 'cart_items': cart_items, 'totalitem': totalitem})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@login_required
def orders(request):
    totalitem = get_items_count_in_cart(request)
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op, 'totalitem': totalitem})


# def payment_completed_view(request):

#    return render(request,'app/payment_completed.html')
# def payment_failed_view(request):

#    return render(request,'app/payment_failed.html')
