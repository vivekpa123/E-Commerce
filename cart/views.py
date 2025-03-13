from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages



# Create your views here.
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})





def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # Test for POST
    if request.POST.get('action') == 'post':

        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to session
        cart.add(product=product, quantity=product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity })
        messages.success(request, "Added To Cart Successfully!")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product ID and quantity
        product_id = int(request.POST.get('product_id'))
        # call delete function in our cart
        cart.delete(product=product_id)

    response =JsonResponse({'product': product_id})
    messages.success(request, "Deleted From Cart Successfully!")
    return response
   



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product ID and quantity
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty', '').strip()

        # Check if product_qty is a valid number
        if not product_qty.isdigit():
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        product_qty = int(product_qty)

        # Update cart
        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Your Cart Has been Updated Successfully!")
        return response

