from django.urls import include, path

from .views import DjUserViewSet

urlpatterns = [
    path('users/<int:id>/subscribe/',
         DjUserViewSet.as_view(), name='subscribe'),
    path('users/subscriptions/', DjUserViewSet.as_view(),
         name='subscription'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
