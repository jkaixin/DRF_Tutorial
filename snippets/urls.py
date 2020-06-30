from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views



urlpatterns = [
    path(r'snippets/', views.SnippetList.as_view()),
    path(r'snippets/<int:pk>/', views.SnippetDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
