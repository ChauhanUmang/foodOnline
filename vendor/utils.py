from vendor.models import Vendor


def get_vendor(request):
    return Vendor.objects.get(user=request.user)