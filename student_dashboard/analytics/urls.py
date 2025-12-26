from django.urls import path
from . import views 


urlpatterns = [
    path("",views.dashboard, name="dashboard"),
    path("upload/",views.upload_data,name="upload_data"),
    path('stats/', views.statistics_view, name='statistics'),
    path("chart/",views.chart_view,name="chart"),
]
