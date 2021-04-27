from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_list, name='articles_list'),
    path('<int:pk>/<slug:slug>/', views.article_detail, name='article_detail'),
    path('like/', views.article_like, name='like'),
    path('create_article/', views.create_article, name='create_article'),
    path('edit/article/<int:post_id>/', views.edit_article, name='edit_article'),
    path('query/<str:action>/<str:arg>/', views.query, name="query"),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('track_user/', views.track_user, name="track"),
    path('ads.txt', views.AdsView.as_view()),

]
