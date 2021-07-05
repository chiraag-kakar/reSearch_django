from django.urls import path
from . import views

urlpatterns = [
    path('clear/',views.indexes,name="indexes"),
    path('index/',views.indexing_document,name="index-docs"),
    path('search/',views.search,name="search"),
    path('doc/<int:id>/',views.retrieve_doc,name="retrieve-document"),
    path('all/',views.retrieve_all,name="retrieve_all"),
]