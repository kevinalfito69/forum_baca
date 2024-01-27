from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/', auth_view.LogoutView.as_view( next_page='postingan'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("profile/<str:username>", userProfileView.as_view(), name="profile"),
    path("<str:username>/follow/<int:user_id>", toggleFollow, name="follow"),
    path("<str:username>/following/", UserFollowingView.as_view(), name="following_list"),
    path("<str:username>/follower/", UserFollowerView.as_view(), name="follower_list"),
    path("<str:username>/change-password/", ChangePassword.as_view(), name="change_password"),
    path("<str:username>/change-profile-picture/", changeProfilePicture.as_view(), name="change_profile_picture"),
    path('list-user/', ListUserView.as_view(),name='list_user'),
]
