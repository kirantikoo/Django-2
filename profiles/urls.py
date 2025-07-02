from django.urls import path
from .views import UpdateProfileView, ProfileDetailView, FollowView

from . import views

app_name = "profiles"

urlpatterns = [
    path('update/', UpdateProfileView.as_view(), name='update_profile'),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),


]
