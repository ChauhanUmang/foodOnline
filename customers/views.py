from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import UserProfile
from accounts.views import check_role_customer
from accounts.forms import CustomerProfileForm, UserInfoForm


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def profile(request):
    existing_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profile_form = CustomerProfileForm(request.POST, request.FILES, instance=existing_profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('cust_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = CustomerProfileForm(instance=existing_profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': existing_profile
    }

    return render(request, 'customers/profile.html', context)

