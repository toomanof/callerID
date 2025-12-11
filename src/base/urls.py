from django.urls import path

from src.base.views.api import CallerIDView
from src.base.views.main import view_call_id

urlpatterns = [
    path('', view_call_id, name='caller_id'),
    path('api/caller-id/<str:phone>', CallerIDView.as_view()),
]