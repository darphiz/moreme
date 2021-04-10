from .models import interest
from articles.models import Article
from django.db.models import Count
from django.db.models import Q
##records the category a user clicks##


def record_interest(user, category):
    if user.is_authenticated:
        try:
            cat_click = interest.objects.get(user=user, category=category)
            cat_click.hits += 1
            cat_click.save()
        except:
            cat_click = interest(user=user, category=category, hits=1)
            cat_click.save()
    else:
        pass


def get_user_interest(user):
    if user.is_authenticated:
        interest_graph = interest.objects.filter(user=user)
        return interest_graph


def rec_news(user, load_article):
    if user.is_authenticated:
        following = user.following.all()
        article_by_follow_load = load_article.filter(author__in=following)
        article_by_follow = article_by_follow_load.annotate(like=Count(
            'users_like')).order_by('-publish', '-like')

        if article_by_follow_load.count() <= 2:  # if articles published by followed authors less than 2
            article_by_follow = load_article.annotate(like=Count(
                'users_like')).order_by('-publish', '-like', )
    return article_by_follow


def rec_top_news(user, load_article):
    if user.is_authenticated:
        intt_list = get_user_interest(user)
        if intt_list.count() >= 3:
            intt = intt_list.values_list('category', flat=True)
            get_top_news = load_article.filter(
                category__id__in=intt)
            get_top_news = get_top_news.annotate(like=Count(
                'users_like')).order_by('-like', '-publish',)
            if get_top_news.count() < 1:
                get_top_news = load_article

        else:
            get_top_news = load_article
    return get_top_news


def rec_editors_pick(user, load_article):
    if user.is_authenticated and get_user_interest(user).count() >= 3:
        intt_list = get_user_interest(user)
        intt = intt_list.values_list('category', flat=True)
        and_lookup = (Q(editors_pick=True) &
                      Q(category__id__in=intt)
                      )
        get_editors_pick = load_article.filter(and_lookup).distinct()
        get_editors_pick = get_editors_pick.annotate(like=Count(
            'users_like')).order_by('-publish', '-like',)

    else:
        get_editors_pick = load_article.filter(editors_pick=True).annotate(
            like=Count('users_like')).order_by('-publish', '-like',)

    return get_editors_pick


def rec_user_cat(user):
    if user.is_authenticated:
        intt_list = get_user_interest(user)
        intt = intt_list.order_by('-hits')[:3]
    return intt