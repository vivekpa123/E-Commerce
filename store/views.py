from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.db.models import Q # Make sure to import Product (not product)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart





def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query The Products Database Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.success(request, "That Product Doesn't Exist")
            return render(request, 'search.html', {})
        else: 
            return render(request, 'search.html', {'searched': searched}) 
    else:
       return render(request, 'search.html', {}) 





def update_info(request):
    if request.user.is_authenticated:
         # Get current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user shipping info
        shipping_user  = ShippingAddress.objects.get(user__id=request.user.id)
        # Get original user form
        form = UserInfoForm(request.POST or None, instance = current_user)
        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save Shipping form
            shipping_form.save()
            messages.success(request, "Your Info Has Been Update..!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form':shipping_form})

    else:
         messages.success(request, "You MUst Be Logged IN ..!")
         return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated..!")
                login(request, current_user)
                return redirect('update_user')  # ✅ Redirect after success
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)  # ✅ Show form errors
                return render(request, 'update_password.html', {"form": form})  # ✅ Return response
        
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {"form": form})  # ✅ Always return render
    
    else:
        messages.error(request, "You Must Be Logged In To View This Page")
        return redirect('home') 

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Update..!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
         messages.success(request, "You MUst Be Logged IN ..!")
         return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})     


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')

    # Look up the category (case-insensitive)
    category = Category.objects.filter(Q(name__iexact=foo)).first()

    if category:
        products = Product.objects.filter(Category__name=category)  # If Category has a 'name' field
        return render(request, 'category.html', {'products': products, 'category': category})
    else:
        messages.error(request, "That category doesn't exist..!!")
        return redirect('home')
     


def product(request, pk):
     product = Product.objects.get(id=pk)  # Fetch all products
     return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'home.html', {'products': products})  # Use 'products' (not 'product')

def about(request):
    return render(request, 'about.html', {}) 

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '')  # Use .get() to avoid KeyError
        password = request.POST.get('password', '')  

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do some Shopping Cart Stuff
            current_user = Profile.objects.get(user__id=request.user.id)

            # Get the saved cart from db
            saved_cart = current_user.old_cart
            # convert db string to python dictionary
            if saved_cart:
               # Convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dicitonary to our session
                # Get the Cart
                cart = Cart(request)
                # Loop Throughthe cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error, Please Try Again")
            return redirect('login')

    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out, Thanks You For Shopping With Us"))
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("Username Created - please fill out your user info below"))
			return redirect('update_info')
	
	return render(request, "register.html", {'form':form})