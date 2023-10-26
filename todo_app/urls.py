from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.Search, name="searchResult"),
    path("sort/<str:sort_param>/", views.Sort, name="sort"),

    path("todo", views.Home, name="home"),
    path("add", views.CreateToDo, name="create"),
    path("edit/<str:id>/", views.GetByIdToDo, name="getById"),
    path("update/<str:id>/", views.UpdateToDo, name="updating"),
    path("delete/<str:id>/", views.DeleteToDo, name="deleting"),

    path("", views.RegisterUser, name="registerUser"),
    path("login", views.LoginUser, name="loginUser"),
    path("logout", views.LogoutUser, name="logoutUser"),
]