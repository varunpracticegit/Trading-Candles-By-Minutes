
from django.contrib import admin
from django.urls import path
from MainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    # path('download_json/<str:filename>', views.download_json, name='download_json'),
]
