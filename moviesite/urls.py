from django.conf import settings
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.movie_list, name='main'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('genre/<int:genre_id>/', views.MoviesByGenre.as_view(), name='movies_by_genre'),
    path('movie/<int:movie_id>/', views.MovieDetail.as_view(), name='movie_detail'),
    path('movie/add/', views.MovieCreate.as_view(), name='movie_create'),
    path('movie/<int:movie_id>/update/', views.MovieUpdate.as_view(), name='movie_update'),
    path('movie/<int:movie_id>/delete/', views.MovieDelete.as_view(), name='movie_delete'),
    path('genre/add/', views.GenreCreate.as_view(), name='genre_create'),
    path('genre/<int:genre_id>/update/', views.GenreUpdate.as_view(), name='genre_update'),
    path('genre/<int:genre_id>/delete/', views.GenreDelete.as_view(), name='genre_delete'),
    path('profile/<str:username>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]