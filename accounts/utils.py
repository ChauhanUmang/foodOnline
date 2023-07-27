from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def detect_user(user):
    if user.role == 1:
        redirect_url = 'vendorDashboard'
    elif user.role == 2:
        redirect_url = 'custDashboard'
    elif user.role is None and user.is_superadmin:
        redirect_url = 'admin'

    return redirect_url


def send_verification_mail(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Email Verification for FoodOnline'
    message = render_to_string('accounts/email/account_verification_email.html',
                               {
                                   'user': user,
                                   'domain': current_site,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': default_token_generator.make_token(user),
                               })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
