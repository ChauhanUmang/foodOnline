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
            # Two ways to save the user.
            # 1. Use form to save user directly
            # 2. use create_user function from UserManager class.

            # Create user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name, last_name, username, email, password)
            user.role = User.CUSTOMER
            user.save()
            # this could be improved. as create_user already saved the user in db and returned that user
            # we are updating one value i.e. role here for that user and saving it again in db.
            # this is creating an extra db hit.
            print("User is created.")
            return redirect('register_user')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)
