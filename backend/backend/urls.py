from django.contrib import admin
from django.urls import path
from rag.views import health
from rag.views import query_rag

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
    path("api/query/", query_rag),
]

