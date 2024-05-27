# yourappname/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('query/', views.query_plot, name='query'),
    path('get_data/', views.get_data, name='get_data' ),
    path('filter_data/', views.filter_data, name='filter_data'),
    path('plot/', views.plot_data, name='plot_data'),
]
