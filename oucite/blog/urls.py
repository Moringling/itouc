from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("article/new/", views.article_create, name="article_create"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("article/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("author/<str:nickname>/", views.add_comment, name="author_articles"),
]