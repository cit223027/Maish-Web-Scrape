from django.urls import path
from .views import LinkList, LinkDetail, SearchLinks, AddLink

urlpatterns = [
    path('links/', LinkList.as_view(), name='link-list'),
    path('links/<int:pk>/', LinkDetail.as_view(), name='link-detail'),
    path('', SearchLinks.as_view(), name='search-links'),
    path('add/', AddLink.as_view(), name='add-link'),
]
