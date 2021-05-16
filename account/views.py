from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from account.form import UserForm, CreatorProfileForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact, CreatorProfile
from articles.models import Article
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

########################################
########################################
########AUTHENTICATION SECTION#########
#######################################


def register(request):
    form_css = True
    registered = False
    user = None

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        cpassword = request.POST.get('cpassword')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # If the two forms are valid...

        if cpassword != password:
            form_error = "password not matching"
            context = {'form_error': form_error,
                       'user_form': user_form, 'profile_form': profile_form, 'form_css': form_css}
            return render(request, 'account/auth/register.html', context)
        elif User.objects.filter(email=email).exists():
            form_error = "Email taken by another user, try another one."
            context = {'form_error': form_error,
                       'user_form': user_form, 'profile_form': profile_form, 'form_css': form_css}
            return render(request, 'account/auth/register.html', context)
        elif user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)

            profile.user = user
            profile.save()
            registered = True

            login(request, user)
            return HttpResponseRedirect(reverse('articles_list'))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    context = {'user_form': user_form,
               'profile_form': profile_form, 'registered': registered, 'form_css': form_css}
    return render(request, 'account/auth/register.html', context)


def register_creator(request):
    form_css = True
    if request.method == 'POST':
        form = CreatorProfileForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            zoo = "Unable to authenticate user, check username and password. Note that you need to create a hub account first before upgrading to a creator account. Still getting this error? send an email to mail.moremehub@gmail.com"
            return render(request, 'account/auth/register_creator.html',
                          {'form': form, 'zoo': zoo, 'form_css': form_css})

        elif CreatorProfile.objects.filter(user=user).exists() == True:
            zoo = "This user already has a creator account"
            return render(request, 'account/auth/register_creator.html',
                          {'form': form, 'zoo': zoo, 'form_css': form_css})
        elif form.is_valid():
            user.profile.is_creator = True
            user.profile.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('dashboard', action='landing')
    else:
        form = CreatorProfileForm()

    return render(request, 'account/auth/register_creator.html', {'form': form, 'form_css': form_css})


def user_login(request):
    form_css = True
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('articles_list'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            form_error = "Invalid login details: {0} | {1}".format(
                username, password)
            return render(request, 'account/auth/login.html', {'form_error': form_error, 'form_css': form_css})
    else:
        return render(request, 'account/auth/login.html', {'form_css': form_css})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('articles_list'))

 ########################################
 ########################################
 ########USER PROFILE SECTION#########
 #######################################


def user_list(request):
    users_list = User.objects.filter(is_active=True).exclude(
        first_name__icontains="Anonymous").order_by('id')
    paginator = Paginator(users_list, 9)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


def user_detail(request, username):
    ajax_here = True
    user = get_object_or_404(User, username=username, is_active=True)
    articles = Article.published.filter(author=user).order_by('-publish')
    return render(request, 'account/user/detail.html', {'user': user, 'articles': articles, 'ajax_here': ajax_here})

 ########################################
 ########################################
 ########FOLLOW/FOLLOWERS SECTION########
 #######################################


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


@login_required
def dashboard(request, action):
    articles = Article.objects.filter(author=request.user)
    acl = Article.published.filter(author=request.user)
    if action == 'landing':
        landing = True
        articles = Article.objects.filter(author=request.user)[:5]
        art = Article.objects.filter(
            author__username='admin', status='published').count()
        context = {'articles': articles, 'landing': landing, 'art': art}
    if action == 'library':
        library = True
        context = {'articles': articles, 'library': library}
    if action == 'money':
        money = True
        y = []
        z =[]
        month_articles = acl.filter(created__gte=timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0))
        this_month = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month = this_month - timedelta(days = 30)
        last_month_articles = acl.filter(created__range=[last_month,this_month])
        last_ppc = last_month_articles.filter(article_type='ppc')
        for article in last_ppc:
            x = article.get_clicks()
            z.append(x)
        last_ppc_revenue = float(sum(z) * 0.06)
        last_ppa_revenue = last_month_articles.filter(article_type='ppa').count() * 500
        last_month_revenue = last_ppc_revenue + last_ppa_revenue
        ppc_articles = month_articles.filter(article_type='ppc')
        for article in ppc_articles:
            x = article.get_clicks()
            y.append(x)
        ppc_revenue = float(sum(y) * 0.06)
        ppa_revenue = month_articles.filter(article_type='ppa').count() * 500
        total_revenue = ppc_revenue + ppa_revenue
        context = {'last_month_revenue':last_month_revenue,'articles': articles, 'money': money,
                   'month_articles': month_articles, 'ppa_revenue': ppa_revenue, 'ppc_revenue': ppc_revenue, 'total_revenue': total_revenue}
    if action == 'account':
        account = True
        context = {'articles': articles, 'account': account}
    if action == 'editorial':
        editorial = True
        articles = Article.objects.filter(
            author__username='admin', status='published')
        context = {'articles': articles, 'editorial': editorial}
    if action == 'activity':
        activity = True
        context = {'articles': articles, 'activity': activity}
    if action == 'feedback':
        feedback = True
        context = {'articles': articles, 'feedback': feedback}
    context['acl'] = acl
    return render(request, 'account/user/dashboard.html', context)
