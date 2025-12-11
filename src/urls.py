from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        '',
        view=include(arg=("src.base.urls", "base"), namespace="base"),
        name='caller_id'
    ),
    path('admin/', admin.site.urls),
]
