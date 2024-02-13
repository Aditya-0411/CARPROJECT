from django.urls import path
from cars import views
from cars.views import CarsViewset, LikeView, CommentsView, RegisterView, LoginView

from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    path('cars/', CarsViewset.as_view() ),
    path('cars/<int:id>/', CarsViewset.as_view() ),
    path('cars/<int:id>/like/', LikeView.as_view(), name='car-like'),
    path('register/' , RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('comments/', CommentsView.as_view(), name='comments-list'),
    path('comments/<int:id>/', CommentsView.as_view(), name='comments-detail'),
    #path('register/' , RegisterView.as_view(), name='register')

]