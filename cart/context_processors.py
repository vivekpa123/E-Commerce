from .cart import Cart

# Create context processor so that our cart can work on all pages of the site
def cart(request):
    # Return the default data from our cart
    return {'cart': Cart(request)}