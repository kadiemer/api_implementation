from django.urls import path
from .views import (
    read_write_alerts,
)

urlpatterns = [
    path("alerts/", read_write_alerts, name="read_write_alerts"),
]
