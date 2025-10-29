from django.urls import path
from .views import PredictView, HealthView, ModelInfoView

urlpatterns = [
    path('health/', HealthView.as_view(), name='health'),
    path('model-info/', ModelInfoView.as_view(), name='model-info'),
    path('predict/', PredictView.as_view(), name='predict'),
]