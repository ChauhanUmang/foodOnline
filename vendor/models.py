from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # means it is updated for this vendor
            # at the time of creation, self.pk will be None.

            # get the current i.e. original details of the vendor here using the pk
            orig = Vendor.objects.get(pk=self.pk)

            # if there is difference in the is_approved status of vendor in the original and
            # updated version
            if orig.is_approved != self.is_approved:

                mail_template = 'accounts/email/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }

                if self.is_approved:
                    # send notification mail
                    mail_subject = 'Congratulation! Your restaurant has been approved.'
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send rejection mail
                    mail_subject = 'We are sorry! You are not eligible for publishing your food menu ' \
                                   'on our marketplace.'
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
