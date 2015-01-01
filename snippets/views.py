from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


#class SnippetList(generics.ListCreateAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
#
#
#class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

# Notice that we've also used the @detail_route decorator to create a custom action, named highlight. 
# This decorator can be used to add any custom endpoints that don't fit into the standard create/update/delete style.

from rest_framework.decorators import detail_route

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user)


from django.contrib.auth.models import User

from snippets.serializers import UserSerializer

# Replaced with ViewSet
#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#
#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework import renderers
from rest_framework.response import Response


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
