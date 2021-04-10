from .models import View, Article
import json
from django.db.models import Count
from news_recommendation.models import Visit


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def record_view(request, article):
    try:
        ip = get_ip(request)
        jsonDec = json.decoder.JSONDecoder()  # Init Json decorder##
        select_article = View.objects.get_or_create(
            article=article)  # get article view object   ##
        get_ip_list = select_article[0].ip_address

        # get list of ips that click the article##
        ip_list = jsonDec.decode(get_ip_list)
        if ip not in ip_list:
            # click is unique the article
            select_article[0].click += 1
            ip_list.append(ip)
            select_article[0].ip_address = json.dumps(ip_list)
            select_article[0].save()
        if request.user.is_authenticated:
            record_visit = Visit.objects.get_or_create(user=request.user)
            record_visit[0].article_visited.add(article)
            record_visit[0].save()
    except:
        pass


def get_similar_post(article, tags):
    try:
        post_tags_ids = tags.values_list(
            'name', flat=True)
        similar_posts = Article.published.filter(
            tag__icontains=post_tags_ids).exclude(id=article.id)
        similar_posts = similar_posts.annotate(same_tags=Count(
            'tag'), like=Count('users_like')).order_by('-same_tags', '-publish', '-like')
        if not similar_posts:
            similar_posts = Article.published.filter(
                category=article.category).exclude(id=article.id)
            similar_posts = similar_posts.annotate(like=Count(
                'users_like')).order_by('-publish', '-like')
    except:
        similar_posts = Article.published.filter(
            category=article.category).exclude(id=article.id)
    return similar_posts


def get_related_post(article):
    related_posts = Article.published.filter(
        category=article.category).exclude(id__in=[article.id])
    related_posts = related_posts.annotate(like=Count(
        'users_like')).order_by('-publish', '-like')
    return related_posts
