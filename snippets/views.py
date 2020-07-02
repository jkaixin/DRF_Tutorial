from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import permissions
from snippets.models import Snippet
from django.contrib.auth.models import User
from snippets.serializers import SnippetsSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class SnippetList(APIView):
    """
    展示所有的snippet，及创建一个新的snippet
    """
    # 确保认证过的 user 有读写权限，没认证的只有读权限
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetsSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class SnippetDetail(APIView):
    """
    展示，更新或删除一个snippet
    """
    # 确保认证过的 user 有读写权限，没认证的只有读权限
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Snippet.objects.get(id=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):        
        snippet = self.get_object(pk)
        serializer = SnippetsSerializer(snippet)

        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    """"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
