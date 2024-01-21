import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Link
from .serializers import LinkSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .forms import LinkForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy


class LinkList(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'author', 'date_published', 'url']


class LinkDetail(generics.RetrieveAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class SearchLinks(generics.ListAPIView):
    serializer_class = LinkSerializer
    common_class_names = ['content-block', 'content', 'article-body', 'mb15', 'core-container', 'field', 'region', 'region-content', ]
    common_tags = ['div', 'section', 'article', 'p', ]

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        results = []

        for link in Link.objects.all():
            try:
                response = requests.get(link.url)
                soup = BeautifulSoup(response.content, 'html.parser')
                content_element = None

                for tag in self.common_tags:
                    for class_name in self.common_class_names:
                        content_element = soup.find(tag, class_=class_name)
                        if content_element:
                            break
                    if content_element:
                        break

                if content_element and search_query.lower() in content_element.get_text().lower():
                    results.append(link)
            except Exception as e:
                print(f"Error processing link {link.url}: {str(e)}")

        return results

    def get(self, request, *args, **kwargs):
        results = self.get_queryset()
        return render(request, 'search_page.html', {'results': results, 'search_query': request.GET.get('search', '')})


class AddLink(CreateView):
    model = Link
    form_class = LinkForm  # Use your LinkForm
    template_name = 'add_link.html'
    success_url = reverse_lazy('add-link')  # Redirect to the same page after successful form submission

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()  # Save the object to the database
        success_message = "Link added successfully!"
        return self.render_to_response(self.get_context_data(form=form, success_message=success_message))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))

