from django.urls import path

from .views import *


urlpatterns = [
    path('', PostinganView.as_view(), name="postingan"),
    path("posting/", TambahPostinganView.as_view(), name="tambah-postingan"),
    path("delete/<int:id>", DeletePostinganView.as_view(), name="hapus-postingan"),
    path("<slug:slug>/edit/<int:id>", EditPostinganView.as_view(), name="edit-postingan"),
    path("detail/<slug:slug>/", DetailPostinganView.as_view(), name="detail-postingan"),
    path('detail/<slug:slug>/tambahkomentar/', TambahKomentar.as_view(), name='tambah-komentar'),
    path('detail/<slug:slug>/hapuskomentar/<int:pk>', HapusKomentar.as_view(), name='hapus-komentar'),
    path('toggle-like/<int:post_id>/', toggleLike, name='toggle-like'),
    path('search/', SearchPostingan.as_view(), name='search-post'),
    path('quotes/',ShowQuotes.as_view(),name = "quotes")
    
]
