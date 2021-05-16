from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from tagging.registry import register
from tagging.fields import TagField
from random import randint
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now
import re
from ckeditor_uploader.fields import RichTextUploadingField


class CategoryManager(models.Manager):

    def new_category(self, category):
        new_category = self.create(category=re.sub('\s+', '-', category)
                                   .lower())

        new_category.save()
        return new_category


class Category(models.Model):

    category = models.CharField(
        verbose_name="Category",
        max_length=250, blank=True,
        unique=True, null=True)
    color_code = models.CharField(
        verbose_name="Color Code",
        max_length=250, blank=True,
        null=True,
        default='bg-primary'
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_total_article(self, category):
        at = Article.objects.filter(category=category)
        total = at.count()
        return total

    @property
    def contain_article(self):
        at = Article.objects.filter(category=self)
        if at.count() < 1:
            return False
        else:
            return True

    def __str__(self):
        return self.category


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')

    def search(self, query):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(body__icontains=query) |
                         Q(slug__icontains=query)
                         )
            # distinct() is often necessary with Q lookups
            qs = qs.filter(or_lookup).distinct()
        return qs


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset()\
            .filter(active=True, status="published")

    def get_articles(self):
        at = self.get_queryset()
        ex_id = []  # initialize an empty list
        for a in at:  # check if loaded article is still relevant
            if a.trend_for == '6h':
                publish_time = a.publish + timedelta(hours=6)
                if publish_time <= now():
                    a.active = False
                    # appends the initial empty list with the ids of irrelevant articles
                    ex_id.append(a.id)
                    a.save()
            elif a.trend_for == '12h':
                publish_time = a.publish + timedelta(hours=12)
                if publish_time <= now():
                    a.active = False
                    # appends the initial empty list with the ids of irrelevant articles
                    ex_id.append(a.id)
                    a.save()
            elif a.trend_for == '1d':
                publish_time = a.publish + timedelta(days=1)
                if publish_time <= now():
                    a.active = False
                    # appends the initial empty list with the ids of irrelevant articles
                    ex_id.append(a.id)
                    a.save()
            elif a.trend_for == '2d':
                publish_time = a.publish + timedelta(days=2)
                if publish_time <= now():
                    a.active = False
                    # appends the initial empty list with the ids of irrelevant articles
                    ex_id.append(a.id)
                    a.save()
            elif a.trend_for == 'no':
                a.active = False  # appends the initial empty list with the ids of irrelevant articles
                ex_id.append(a.id)
                a.save()

        # exclude the irrelevant articles from the list
        at_list = at.exclude(id__in=ex_id)
        return at_list


class Article(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('published', 'Published'),
        ('rejected', 'Rejected')
    )
    TREND_CHOICES = (
        ('unlimited', 'unlimited'),
        ('6h', '6h'),
        ('12h', '12h'),
        ('1d', '1d'),
        ('2d', '2d'),
        ('no', 'No')
    )
    A_TYPE_CHOICES = (
        ('ppa','PPA'),
        ('ppc','PPC')
    )
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author', blank=True, null=True)
    body = models.TextField()
    tag = TagField()
    image_upload = models.ImageField(upload_to="pics")
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Category", on_delete=models.CASCADE)
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    article_type = models.CharField(max_length=10, null=True, blank=True,
                                    choices=A_TYPE_CHOICES, default=A_TYPE_CHOICES[0][0])
    status = models.CharField(max_length=10, null=True, blank=True,
                              choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    article_type = models.CharField(max_length=10, null=True, blank=True,
                                    choices=A_TYPE_CHOICES, default=A_TYPE_CHOICES[0][0])
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='articles_liked',
                                        blank=True)
    trend_for = models.CharField(
        max_length=10, choices=TREND_CHOICES, blank=True, null=True, default=TREND_CHOICES[0][0])
    editors_pick = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    revise = models.BooleanField(default=False)
    updating_article = models.BooleanField(default=False)
    reject_reason = models.CharField(
        max_length=200, blank=True, null=True, default='Your article violates publishing guildlines')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager
    is_active = ActiveManager()  # Our custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    ##Generating A unique slug##

    def save(self, *args, **kwargs):
        if not self.updating_article:
            if Article.objects.filter(title=self.title).exists():
                extra = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + extra
            else:
                self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail',
                       kwargs={'pk': self.pk, 'slug': self.slug})

    def get_clicks(self):
        try:
            at = View.objects.get(article=self)
            clicks = at.click
        except:
            clicks = 0
        return clicks

    def get_comments(self):
        try:
            at = Comment.objects.filter(article=self)
            comments = at.count()
        except:
            comments = 0
        return comments


####COMMENT SECTION #####


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(blank=True, null=True,
                            max_length=250, default="ANON")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.article)

######  VIEW COUNTER #####


class View(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
    click = models.IntegerField(default=0)
    ip_address = models.TextField(default='[]')

    def __str__(self):
        return self.article.title


class Subscriber(models.Model):
    email = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class AdsManager(models.Manager):
    def get_queryset(self):
        return super(AdsManager, self).get_queryset()\
            .filter(active=True)

class Advertise(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='categories', blank=True, null=True)
    ad_image = models.ImageField(upload_to="ads")
    link = models.URLField()
    desc = models.CharField(max_length=250)
    active = models.BooleanField(default = False)
    objects = models.Manager()  # The default manager.
    is_active = AdsManager()

    def __str__(self):
        return self.desc
