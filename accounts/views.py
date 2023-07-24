from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User


# Create your views here.
def register_user(request):
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            return redirect('register_user')
    else:
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/registerUser.html', context)
