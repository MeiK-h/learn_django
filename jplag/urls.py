from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'jplag'
urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
     path('<int:pk>/', views.CheckerView.as_view(), name='checker'),
     path('new_checker/', views.new_checker, name='new_checker'),
     path('<int:pk1>/<int:pk2>/delete_code/', views.delete_code, name='delete_code'),
     path('<int:pk>/upload_code/', views.upload_code, name='upload_code'),
     path('<int:pk>/run/', views.run_jplag, name='run_jplag'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
