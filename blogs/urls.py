from django.urls import path
from .views import *

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create-blog'),
    path('list/', BlogListView.as_view(), name='blog-list'),
    path('edit/<int:pk>/', BlogEditView.as_view(), name='blog-edit'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='entry-list'),
    path('detail/<int:pk>/upload/', upload_entry_from_file, name='upload-entry'),
    path('entry/<int:pk>/create/', EntryCreateView.as_view(), name='create-entry'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='detail-entry'),
    path('entry/<int:pk>/edit/', EntryEditView.as_view(), name='edit-entry'),
    path('', MainPageView.as_view(), name='main'),
]
