from django.urls import path
from .views import (
    MainView, AboutView, MoviesByGenre, MovieDetail,
    MovieCreate, MovieUpdate, MovieDelete,
    ProfileDetail, ProfileView,
    register_view, login_view, logout_view
)

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("about/", AboutView.as_view(), name="about"),
    path("movie/add/", MovieCreate.as_view(), name="add_movie"),
    path("movie/<int:movie_id>/update/", MovieUpdate.as_view(), name="update_movie"),
    path("movie/<int:movie_id>/delete/", MovieDelete.as_view(), name="delete_movie"),
    path("movie/<int:movie_id>/", MovieDetail.as_view(), name="by_movie"),
    path("genre/<int:genre_id>/", MoviesByGenre.as_view(), name="by_genre"),
    path("profile/<str:username>/", ProfileDetail.as_view(), name="profile_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
