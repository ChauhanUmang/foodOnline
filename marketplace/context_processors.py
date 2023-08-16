from marketplace.models import Cart
from menu.models import Product


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    subtotal = 0
    pickup_fee = 10
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.products.id)
            subtotal += (product.price * item.quantity)
            subtotal = round(subtotal, 2)

        tax = round(float(0.13) * float(subtotal + pickup_fee), 2)
        grand_total = round(float(subtotal) + float(pickup_fee) + float(tax), 2)
    return dict(subtotal=subtotal, pickup_fee=pickup_fee, tax=tax, grand_total=grand_total)