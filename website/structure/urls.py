from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index') ,
    path('topics', views.topics, name='topics'),
    path('topics/<topic_id>/', views.topic, name='topic') ,
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_entry/<entry_id>/', views.delete_entry, name='delete_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('entry/<int:entry_id>/add_collaborator/', views.add_collaborator, name='add_collaborator'),
    path('entry/<int:entry_id>/remove_collaborator/', views.remove_collaborator, name='remove_collaborator'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]


