from django.urls import path
from . import views

urlpatterns = [
    path('all_people/', views.PersonListView.as_view(), name='all_people'),
    path('person/<int:pk>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('delete_person/<int:pk>/', views.PersonDeleteView.as_view(), name='delete_person'),
    path('create_person/', views.create_person, name='create_person'),
    path('update_person/<int:pk>/', views.update_person, name='update_person'),
]