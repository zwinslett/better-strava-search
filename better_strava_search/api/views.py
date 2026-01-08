from django.shortcuts import render
from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer
import requests
import json
import envs


# Create your views here.
class AllActivities(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class SearchResults(generics.ListAPIView):
    def get_queryset(self):
        solr_url = f'{envs.solr_core}/select?'
        query = self.request.GET.get('q', '')
        field = self.request.GET.get('field', '')
        solr_query = f"{field}:{query}"
        solr_params = {
            'q': solr_query,
            'wt': 'json',
            'rows': 100,
        }
        try:
            response = requests.get(solr_url, params=solr_params, timeout=10)
            response.raise_for_status()
            docs = response.json()['response']['docs']

            ids = [docs['id'] for docs in docs]
            qs = Activity.objects.filter(id__in=ids)
        except:
            qs = Activity.objects.none()
        return qs

    serializer_class = ActivitySerializer
