from django.urls import path
from . import views

urlpatterns = [
    path('', views.peminjaman_list, name='peminjaman_list'),
    path('tambah/', views.peminjaman_create, name='peminjaman_create'),
    path('<int:id>/', views.peminjaman_detail, name='peminjaman_detail'),
    path('<int:id>/edit/', views.peminjaman_update, name='peminjaman_update'),
    path('<int:id>/hapus/', views.peminjaman_delete, name='peminjaman_delete'),
    path('<int:id>/kembalikan/', views.peminjaman_kembalikan, name='peminjaman_kembalikan'),
]