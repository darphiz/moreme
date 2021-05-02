from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from news_recommendation.models import interest
from articles.models import Category
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.conf import settings
from django.http import HttpResponse
from ckeditor_uploader.fields import RichTextUploadingField

class AccountManager(models.Manager):
    def get_queryset(self):
        return super(AccountManager, self).get_queryset()\
            .filter(is_approved=True)

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(channel_name__icontains=query) |
                         Q(bio__icontains=query) |
                         Q(user__username__icontains=query) |
                         Q(user__first_name__icontains=query) |
                         Q(user__last_name__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


# Create your models here.
class CreatorProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=15, unique=True)
    channel_name = models.CharField(max_length=15, unique=True)
    bio = models.CharField(max_length=150, default="A newshub content creator")
    bank_name = models.CharField(max_length=30, blank=True, null=True)
    acct_number = models.CharField(max_length=30, blank=True, null=True)
    acct_name = models.CharField(max_length=30, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    objects = models.Manager()  # The default manager.
    creator = AccountManager()  # Our custom manager

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_img", blank=True)
    is_creator = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    def get_interest(self):
        intr = interest.objects.filter(user=self.user).order_by('hits')
        intr = intr.values_list('category__category', flat=True)
        intrd = Category.objects.filter(category__in=intr)
        return intrd

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey(
        'auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        'auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField(
    'self', through=Contact, related_name='followers', symmetrical=False))


class BulkMail(models.Model):
    MAIL_TYPE= (
        ('tcc','To All Creators'),
        ('tam','To All Members')
    )
    subject = models.CharField(max_length=150, default="Moreme Hub")
    message = RichTextUploadingField(config_name='default', blank=True, null =True)
    type = models.CharField(max_length=10, null=True, blank=True,
                                    choices=MAIL_TYPE, default=MAIL_TYPE[0][0])
    already_sent = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        subject = self.subject
        message = self.message
        if self.type == 'tam':
            x = []
            for use in User.objects.all():
                mail = use.email
                x.append(mail)
        else:
            x = []
            for use in CreatorProfile.objects.filter(is_approved = True, banned = False ):
                mail = use.user.email
                if mail:
                    x.append(mail)
        recipient = x
        if not self.already_sent == True:
            try:
                msg = EmailMessage(subject, message, "Darphiz at Moremehub <mail.moremehub@gmail.com>", recipient)
                msg.content_subtype = "html"
                msg.send()
                self.already_sent = True
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        super(BulkMail, self).save(*args, **kwargs)