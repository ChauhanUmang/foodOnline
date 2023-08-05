from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from accounts.views import check_role_vendor
from menu.forms import CategoryForm
from menu.models import Category, Product
from vendor.utils import get_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'menu/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(vendor=vendor, category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'menu/products_by_category.html', context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            print(category.category_name)
            # Before finally saving the form, we need to get vendor and slug details
            category.vendor = get_vendor(request)
            category.slug = slugify(category.category_name)
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('menu_builder')
    else:
        form = CategoryForm
    context = {
        'form': form,
    }
    return render(request, 'menu/category/add.html', context)
