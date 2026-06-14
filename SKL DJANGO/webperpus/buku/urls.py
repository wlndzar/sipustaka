from django.urls import path
from . import views



urlpatterns = [
    path('', views.buku_list, name='buku_list'),
    path('tambah/', views.buku_create, name='buku_create'),
    path('<int:id>/', views.buku_detail, name='buku_detail'),
    path('<int:id>/edit/', views.buku_update, name='buku_update'),
    path('<int:id>/hapus/', views.buku_delete, name='buku_delete'),
]