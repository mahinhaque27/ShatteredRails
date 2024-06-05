#All of the import statements
from django.urls import path
from .views import user_login, success, index_2
from .views import forgot_password
from .views import forgot_username
from .views import activate
from . import views

from . import views
#This will be all of the urls for the application
urlpatterns = [
    path("", views.index, name="index"),  #this will lead to the home page (default page)
    path("index2/", views.index_2, name="index_2"),  #this will lead to the second home page (shattered rails 1)
    path("login/", user_login, name="login"), #This is the url to the login page
    path("login/", views.user_login, name = "login"),
    path("logout/", views.user_logout, name="logout"),
    
    path('success/', success, name='success'),
    path("register/", views.register, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("game/", views.game, name="game"), #This is the url for game1
    path("game2/", views.game_2, name="game_2"), #This is the url for game2
    path("profile/", views.profile, name="profile"),
    path("profile/password", views.profilePassword, name="profile-password"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("edit-password/", views.edit_password, name="edit-password"),
    path("save_game_state/", views.save_game_state, name="save_game_state"),
    path("start/", views.start, name="start"),
    path("start1/", views.start1, name="start1"),
    path("help/", views.help, name="help"),
    path('get_progress/', views.get_progress, name='get_progress'),
    path('delete-account/', views.delete_account, name='delete-account'),
        
    path('send_reset_email/', views.send_reset_email, name='send_reset_email'),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('update_password/', views.update_password, name='update_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('forgot-username/', forgot_username, name='forgot_username'),
]
