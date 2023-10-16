from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ArticleViewSet

# Create a router
router = DefaultRouter()

# Register your viewsets with the router and explicitly specify the basename
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    # Include the router's URLs into your project's URLs
    path('', include(router.urls)),
]