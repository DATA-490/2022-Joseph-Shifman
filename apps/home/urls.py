
from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.recall_dash, name='home'),

    path('dashboard.html', views.recall_dash),

    path('recallsearch.html', views.recallsearch_1),
    path('recall/search/year', views.recallsearch_2),
    path('recall/search/year/make', views.recallsearch_3),
    path('recall/search/results', views.recallsearch_results),

    path('ratingsearch.html', views.ratingsearch_1),
    path('rating/search/year', views.ratingsearch_2),
    path('rating/search/year/make', views.ratingsearch_3),
    path('rating/search/year/make/model', views.ratingsearch_4),
    path('rating/search/results', views.ratingsearch_results),

    path('addcar/', views.addcar),
    path('settings.html', views.settings, name='settings'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
