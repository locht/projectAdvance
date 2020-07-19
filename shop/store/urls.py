from django.conf.urls import url 

from . import views 
from django.contrib.auth import views as auth_views

# app_name = 'store'
urlpatterns = [ 
    url(r'^$', views.store, name='store'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    
    url(r'^update_item/', views.updateItem, name='update_item'),
    url(r'^process_order/', views.processOrder, name='process_order'),

    url(r'^larmes/', views.larmes, name='larmes'),
    url(r'^casio/', views.casio, name='casio'),
    url(r'^citizen/', views.citizen, name='citizen'),
    url(r'^daumier/', views.daumier, name='daumier'),
    url(r'^done/', views.done, name='done'),

    url(r'^register/', views.register, name='register'),
    url(r'^register-done/', views.register_done, name='register-done'),
    url(r'^profile/', views.view_profile, name='profile'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
]