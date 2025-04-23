from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('categories/<path:category>', views.category, name='category'),
    path('articles/<int:pk>/<int:author_id>/<int:subject_id>/', views.record, name='record'),
    path('articles/edit/<int:pk>/<int:author_id>/<int:subject_id>/', views.edit_record, name='edit_record'),
    path('articles/<int:author_id>/', views.articles_by_author, name='articles_by_author'),
    path('articles/portal', views.portal_do_autor, name='portal_do_autor'),
    path('articles/portal/meus_artigos', views.meus_artigos, name='meus_artigos'),
    path('articles/portal/novo_artigo', views.novo_artigo, name='novo_artigo'),
]
