from django.conf.urls import url 

from . import views 

# app_name = 'store'
urlpatterns = [ 
    url(r'^$', views.store, name='store'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    
    url(r'^update_item/', views.updateItem, name='update_item'),
    url(r'^process_order/', views.processOrder, name='process_order'),
]