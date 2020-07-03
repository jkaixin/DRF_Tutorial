from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views


urlpatterns = [
    path(r'', views.api_root),
    path(r'snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path(r'snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path(r'snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    path(r'users/', views.UserList.as_view(), name='user-list'),
    path(r'users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
