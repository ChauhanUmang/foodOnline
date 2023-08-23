from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from vendor.forms import VendorForm, OpeningHourForm
from vendor.models import Vendor, OpeningHour
from vendor.utils import get_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
# Create your views here.
def profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=userprofile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
    }

    return render(request, 'vendor/profile.html', context)


def opening_hours(request):
    open_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': open_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)


def add_opening_hours(request):
    # handle the data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            if is_closed == 'True':
                is_closed = True
            else:
                is_closed = False

            print(f'Day is {day}')
            print(f'from_hour is {from_hour}')
            print(f'to_hour is {to_hour}')
            print(f'is closed is {is_closed}')

            try:
                # Check if an entry is there for that day.
                existing_hour = OpeningHour.objects.get(vendor=get_vendor(request), day=day)
                print('Step 1')
                # Condition 1
                if is_closed:
                    print('Step - 2')
                    if existing_hour.from_hour or existing_hour.to_hour:
                        # means from_hour and to_hour have some values
                        response = {'status': 'Failed', 'message': 'Opening Hours already exists for this day!'}
                    else:
                        response = {'status': 'Failed', 'message': 'Already marked as Closed Day.'}
                else:
                    # from_hour and to_hour are present
                    if existing_hour.is_closed:
                        response = {'status': 'Failed', 'message': 'This is already marked as a closed day.'}
                    else:
                        if existing_hour.from_hour <= to_hour and from_hour <= existing_hour.to_hour:
                            response = {'status': 'Failed', 'message': 'Overlapping Opening Hours.'}

                return JsonResponse(response)
            except:
                try:
                    hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour,
                                                      to_hour=to_hour, is_closed=is_closed)
                    if hour:
                        day = OpeningHour.objects.get(id=hour.id)
                        if day.is_closed:
                            response = {'status': 'Success', 'id': hour.id, 'day': day.get_day_display(),
                                        'is_closed': 'Closed'}
                        else:
                            response = {'status': 'Success', 'id': hour.id, 'day': day.get_day_display(),
                                        'from_hour': from_hour, 'to_hour': to_hour}
                    return JsonResponse(response)
                except IntegrityError as e:
                    return JsonResponse({'status': 'Failed', 'message': from_hour + ' - ' + to_hour
                                                                        + ' already exists for this day!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})


def validate_opening_hours(request):
    day = request.POST.get('day')
    from_hour = request.POST.get('from_hour')
    to_hour = request.POST.get('to_hour')
    is_closed = request.POST.get('is_closed')

