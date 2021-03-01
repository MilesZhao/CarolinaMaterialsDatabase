"""carolina_mat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home.views import home_view,search_view,forum_view,contact_view,term_view,doc_view
from entry.views import mat_detail_view,EntryDetailView,demo_view
 
urlpatterns = [
    path('', home_view, name='home'),
    path('entry/', include('entry.urls')),
    path('search/', search_view, name='search'),
    path('forum/', forum_view, name='forum'),
    path('contact/', contact_view, name='contact'),
    path('terms/', term_view, name='terms'),
    path('docs/', doc_view, name='docs'),
    path('results/', mat_detail_view, name='results'),
    path('demo/', demo_view, name='demo'),
    path('admin/', admin.site.urls),
]
