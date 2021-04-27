from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Article, Category, Subscriber, Advertise
from news_recommendation.utils import record_interest, get_user_interest, rec_news, rec_top_news, rec_editors_pick, rec_user_cat
from news_recommendation.models import Visit
from tagging.models import Tag
from .forms import ArticleForm, CommentForm
from django.db.models import Count
from .utils import record_view, get_similar_post, get_related_post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from itertools import chain
from account.models import CreatorProfile
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponse
from django.views import View


##ads##


class AdsView(View):
    def get(self, request, *args, **kwargs):
        line  =  "google.com, pub-8164139980360647, DIRECT, f08c47fec0942fa0"
        return HttpResponse(line)

def articles_list(request):
    # At first Load all active articles
    articles = Article.is_active.get_articles()
    user = request.user
    # init an empty list of articles for you and editors pick
    e_id = []
    for_you_id = []
    # try to get list of articles visited by the user
    try:
        already_visited = Visit.objects.get(
            user=user).article_visited.all()
        already_visited = already_visited.values_list('id', flat=True)
    # If an error occured, probably a new user or an anon
    # then init an empty list
    except:
        already_visited = []
    u_editors_pick = rec_editors_pick(user, articles).exclude(
        id__in=already_visited)
    editors_pick = sorted(
        u_editors_pick, key=lambda a: a.get_clicks(), reverse=True)[:6]

    # append the already init empty editors pick with the id of the loaded articles
    for artic in editors_pick:
        e_id.append(artic.id)

    if user.is_authenticated and get_user_interest(user).count() >= 3:
        unsorted_for_you = rec_news(user, articles).exclude(
            id__in=already_visited)
        # if the articles in for you is less than five
        # then just load all active articles
        if unsorted_for_you.count() < 5:
            unsorted_for_you = articles.annotate(like=Count(
                'users_like')).order_by('?', '-like', ).exclude(id__in=already_visited)
        for_you = sorted(
            unsorted_for_you, key=lambda a: a.get_clicks(), reverse=True)[:5]

        for artic in for_you:
            for_you_id.append(artic.id)
        q_set = list(set(for_you_id).union(already_visited))

        unsorted_recommended = rec_top_news(
            user, articles).exclude(id__in=q_set)
        recommended = sorted(
            unsorted_recommended, key=lambda a: a.get_clicks(), reverse=True)[:5]
    else:
        article = articles.filter(editors_pick=False).order_by('?')
        for_you = article[:5]
        for artic in for_you:
            for_you_id.append(artic.id)

        unsorted_recommended = article.exclude(id__in=for_you_id)
        recommended = sorted(
            unsorted_recommended, key=lambda a: a.get_clicks(), reverse=True)
    if len(recommended)<=3 or len(for_you) <= 3:
        recommended = articles.order_by('-publish')
        for_you = articles.order_by('?')

    context = {"articles": articles,
               "for_you": for_you, "recommended": recommended, 'editors_pick': editors_pick, }
    return render(request, 'index.html', context)


def rec_ad(cat):
    ads =Advertise.is_active.filter(category=cat).order_by('?')[:1]
    if not ads:
        ads = Advertise.is_active.order_by('?')[:1]
    return ads
def article_detail(request, slug, pk):
    ajax_here = True
    article = get_object_or_404(Article, slug=slug, id=pk)
    ads = rec_ad(article.category)
    try:
        already_visited = Visit.objects.get(
            user=request.user).article_visited.all()
        already_visited = already_visited.values_list('id', flat=True)
    except:
        already_visited = []
    if article.status != 'published' and article.author != request.user:
        raise Http404('Permission Denied')
    tags = Tag.objects.get_for_object(article)
    # Get the tag of the particular post###
    c_list = []
    ct = Category.objects.all()
    for c in ct:
        if Article.objects.filter(category=c).count() > 0:
            c_list.append(c)
    cat = c_list

    similar_posts = get_similar_post(article, tags).exclude(
        id__in=already_visited)[:5]

    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'detail.html', {'article': article, 'ajax_here': ajax_here, 'tags': tags, 'cat': cat, 'comments': comments,
                                           'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts,'ads': ads,})


@ login_required
def create_article(request):
    cat = Category.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.author = request.user
            post_item.save()
            return redirect('dashboard', action='landing')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form, 'cat': cat})


def edit_article(request, post_id=None):
    item = get_object_or_404(Article, id=post_id)
    if item.revise != True or item.author != request.user:
        raise Http404('Permission Denied')
    cat = Category.objects.all()
    form = ArticleForm(request.POST or None,
                       request.FILES or None, instance=item)
    if form.is_valid():
        post_item = form.save(commit=False)
        post_item.author = request.user
        post_item.status = 'pending'
        post_item.save()
        return redirect('dashboard', action='landing')
    return render(request, 'add_article.html', {'form': form, 'cat': cat})


@ ajax_required
@ login_required
@ require_POST
def article_like(request):
    if request.user.is_authenticated:
        article_id = request.POST.get('id')
        action = request.POST.get('action')
        if article_id and action:
            try:
                article = Article.objects.get(id=article_id)
                if action == 'like':
                    article.users_like.add(request.user)
                else:
                    article.users_like.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except:
                pass
    return JsonResponse({'status': 'ko'})


def query(request, action, arg):
    ajax_here = True
    if action == 'category':
        results = Article.published.filter(category__category=arg)
        results = results.annotate(like=Count(
            'users_like')).order_by('-publish', '-like')
    if action == 'tag':
        results = Article.published.filter(tag__icontains=arg)
        results = results.annotate(like=Count(
            'users_like')).order_by('-publish', '-like')
    if action == 'explore':
        articles = Article.is_active.get_articles()
        try:
            already_visited = Visit.objects.get(
                user=request.user).article_visited.all()
            already_visited = already_visited.values_list('id', flat=True)
        except:
            already_visited = []
        results = articles.annotate(like=Count(
            'users_like')).order_by('-like', '-publish').exclude(id__in=already_visited)
    if action == "search":
        arg = request.GET['search_query']
        if arg is not None:
            blog_results = Article.published.search(arg)
            user_results = CreatorProfile.creator.search(arg)

            # combine querysets
            queryset_chain = chain(
                blog_results,
                user_results
            )
            results = sorted(queryset_chain,
                             key=lambda instance: instance.pk,
                             reverse=True)
            count = len(results)  # since qs is actually a list
    #Pagination##

    paginator = Paginator(results, 8)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        results = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            #   return an empty page
            return HttpResponse('')
            # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'query_ajax.html', {"action": action, "results": results, "arg": arg, "ajax_here": ajax_here})

    return render(request, 'query.html', {"action": action, "results": results, "arg": arg, "ajax_here": ajax_here})


@ ajax_required
@ require_POST
def track_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        article = Article.objects.get(id=id)
        # Record user interest##
        record_interest(request.user, article.category)
        record_view(request, article)  # Record Clicks on post##
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ko'})


def about(request):
    unsorted_top_channel = CreatorProfile.objects.filter(is_approved=True)
    top_channel = sorted(
        unsorted_top_channel, key=lambda a: a.user.followers.count(), reverse=True)[:3]

    return render(request, 'about.html', {'top_channel': top_channel})


def privacy_policy(request):
    return render(request, 'privacy.html',)

def handler404(request, exception, template_name="404.html"):
    response = render(request,template_name,)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request,'500.html', {},)
    response.status_code = 500
    return response