from django.conf.urls import patterns, url, include
from snippets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
  url(r'^', include(router.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)