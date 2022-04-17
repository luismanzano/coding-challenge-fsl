from django.urls import path

from heyurl import views

urlpatterns = [
    #path('short_url/', views.short_url, name='short_url'),
    path('store/', views.store, name='store'),
    path('', views.redirect, name='redirect'),
    path('/data/', views.data_panel, name='data_panel')
]
