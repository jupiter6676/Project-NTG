
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path('',views.index, name="index"),
    path('create/',views.create, name="create"),
    path('<int:pk>/',views.detail, name="detail"),
    path('<int:pk>/update/',views.update, name="update"),
    path('<int:pk>/delete/',views.delete, name="delete"),
    path('<int:article_pk>/comments_create/',views.comments_create, name="comments_create"),
    path('<int:article_pk>/comments_create/<int:comment_pk>/delete/',views.comments_delete, name="comments_delete"),
]