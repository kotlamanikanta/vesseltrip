"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstApp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    path("get_sensor_data/", get_sensor_data, name="get_sensor_data"),
    path("timespan/", timespan, name="timespan"),
    path("sensor_data/", sensor_data, name="sensor_data"),
    path("sensor_data_avg/", sensor_data_avg, name="sensor_data_avg"),
    path("boatsensor_data_avg/", boatsensor_data_avg, name="boatsensor_data_avg"),
    path("trip_sensors/", trip_sensors, name="trip_sensors"),
]
