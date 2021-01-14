from django.urls import path, include
from . import views

urlpatterns = views.TransactionCRUDL().as_urlpatterns()