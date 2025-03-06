from django.urls import path
from webapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/register/", views.register, name="register"),
    path("api/login/", views.login_user, name="login"),
    path("api/logout/", views.logout_user, name="logout"),
    path("api/list/", views.modules_list, name="list"),
    path("api/view/", views.view_ratings, name="rate"),
    path("api/average/<str:professor_id>/<str:module_code>/", views.view_prof_module_ratings, name="average"),
    path("api/rate-professor/", views.rate_professor, name="rate"),
]
