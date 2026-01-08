from django.urls import path
from . import views
urlpatterns = [
    path('api/activities/', views.AllActivities.as_view(), name="all-activities-api"),
    path('api/activities/search/', views.SearchResults.as_view(), name="search-api"),
]