from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderdItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime

# Create your views here.

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the Order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderdItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped = now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')


        return render(request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.success(request, "Access denied..!")
        return redirect ('home')
         


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        
        if request.method == "POST":
            status = request.POST.get('shipping_status')
            num = request.POST.get('num')

            try:
                # Get the specific order
                order = Order.objects.get(id=num)
                
                # Grab Date and Time
                now = datetime.datetime.now()
                
                # Update order
                order.shipped = True
                order.date_shipped = now
                order.save()

                messages.success(request, "Shipping Status Updated")
                return redirect('home')

            except Order.DoesNotExist:
                messages.error(request, "Order not found.")
        
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    
    else:
        messages.error(request, "Access denied..!")
        return redirect('home')
    


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
         orders = Order.objects.filter(shipped=True)
         if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order =Order.objects.filter(id=num)
            # Grab Date and Time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=False)
            # redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
         return render( request,  "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access denied..!")
        return redirect ('home')






def process_order(request):
    if request.POST:
           # Get the Cart 
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing info from last page
        payment_form = PaymentForm(request.POST or None)

        # Get shipping session data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email =  my_shipping['shipping_email']

        # Create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Oreder
        if request.user.is_authenticated:
            # Logged In
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add Order items
            # Get the order id
            order_id = create_order.pk
            # Get product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderdItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
            # Delete Our Cart

            for key in list(request.session.keys()) :
                if key == "session_key":
                    # Delete the key
                    del request.session[key]   

            # Delete cart from db
            current_user = Profile.objects.filter(user__id=request.user.id) 
            # Delete shopping cart in database
            current_user.update(old_cart="")

            messages.success(request, "Order placed..!")
            return redirect ('home')


        else:
            # Not logged In 
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

             # Add Order items
            # Get the order id
            order_id = create_order.pk
            # Get product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderdItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            for key in list(request.session.keys()) :
                if key == "session_key":
                    # Delete the key
                    del request.session[key]    



            messages.success(request, "Order placed..!")
            return redirect ('home')

    else:
        messages.success(request, "Access Denied")
        return redirect ('home')





def billing_info(request):

    if request.POST:
       # Get the Cart 
       cart = Cart(request)
       cart_products = cart.get_prods
       quantities = cart.get_quants
       totals = cart.cart_total()
       #  Create a session with shipping info
       my_shipping = request.POST
       request.session['my_shipping'] = my_shipping

        
        
       # Check To See If User Is LoggedIn
       if request.user.is_authenticated:
           # Get the billing Form
           billing_form = PaymentForm()
           return render( request,  "payment/billing_info.html",  {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info":request.POST,  "billing_form":billing_form})
       else:
           # Not LoggedIn
            # Get the billing Form
           billing_form = PaymentForm()
           return render( request,  "payment/billing_info.html",  {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info":request.POST,  "billing_form":billing_form})

       shipping_form = request.POST
       return render( request,  "payment/billing_info.html",  {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect ('home')



def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    shipping_user = None  # Initialize shipping_user
    
    if request.user.is_authenticated:
        # Fetch Shipping User
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = None  # If no shipping address exists

        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)

    return render(
        request, 
        "payment/checkout.html", 
        {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form}
    )

    


def payment_success(request):
    return render(request, "payment/payment_success.html", {})
