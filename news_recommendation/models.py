from django.db import models
from django.contrib.auth.models import User
from articles.models import Category, Article


class interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Category", on_delete=models.CASCADE)
    hits = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username


class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_visited = models.ManyToManyField(Article,
                                             related_name='articles_visits',
                                             blank=True)

    def __str__(self):
        return self.user.username
