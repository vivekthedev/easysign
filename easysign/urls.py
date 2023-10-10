from django.contrib.auth.views import LoginView, LogoutView
from .views import Home, UserCreate, UserEdit,process_doc, get_text
from django.urls import path


urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup/", UserCreate.as_view(), name='signup'),
    path("update/<int:pk>", UserEdit.as_view(), name='update'),
    path("document/<str:doc_id>",process_doc, name="document"),
    path("get_text/<int:action>/<str:doc_id>", get_text, name='get_text'),
]
