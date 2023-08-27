from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import UserProfile
from accounts.views import check_role_customer
from accounts.forms import UserProfileForm, UserInfoForm


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def profile(request):
    existing_profile = get_object_or_404(UserProfile, user=request.user)
    profile_form = UserProfileForm(instance=existing_profile)
    user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form
    }

    return render(request, 'customers/profile.html', context)

