from django.urls import path 
from .views import search_decisions
urlpatterns = [
    path("", search_decisions, name="search-decisions"),
    # Bu uygulamanın ana adresine gelen isteği search_decisions fonksiyonuna yönlendirir.
]