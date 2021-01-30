from django.urls import path

from .views import EntryDetailView

app_name = 'entry'
urlpatterns = [
    path('<int:id>/', EntryDetailView.as_view(), name='detail'),
]