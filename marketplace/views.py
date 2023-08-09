from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from marketplace.context_processors import get_cart_counter
from marketplace.models import Cart
from menu.models import Category, Product
from vendor.models import Vendor


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    # We have Products model have foreign key relationship to Category model
    # but we do not have Category model having any relationship with Products
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('product', queryset=Product.objects.filter(is_available=True))
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                prod = Product.objects.get(id=product_id)
                # Check if the user has already added product in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, products=prod)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse(
                        {'status': 'Success',
                         'message': 'Product increased in cart.',
                         'cart_counter': get_cart_counter(request),
                         'qty': chkCart.quantity}
                    )
                except:
                    chkCart = Cart.objects.create(user=request.user, products=prod, quantity=1)
                    return JsonResponse(
                        {'status': 'Success',
                         'message': 'Product added to the cart.',
                         'cart_counter': get_cart_counter(request),
                         'qty': chkCart.quantity}
                    )
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please login to continue.'})
