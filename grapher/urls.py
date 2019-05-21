from django.urls import path
from . import views
#from .views import FCreate
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import redirect_root
''
urlpatterns = [
    path('', views.FormPost, name='input'),
    path('interactive_results/', views.FormGet, name='results'),
    path('png_results/', views.FormGet, name='png_results'),
    path('png_results/final/',views.newView, name='final'),
    path('png_results/product/', views.imagedisplay, name='product')
]


(r'^charts/simple.png$', 'myapp.views.charts.simple')
'''

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = [
   url(r'^connection/',TemplateView.as_view(template_name = 'login.html')),
   url(r'^login/', 'login', name = 'login')
]
'''
