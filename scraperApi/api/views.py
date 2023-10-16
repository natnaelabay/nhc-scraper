from rest_framework import viewsets
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()

        is_parsed = self.request.query_params.get('is_parsed', None)

        if is_parsed is not None:
            queryset = queryset.filter(is_parsed=True if is_parsed == "True" else False)

        return queryset