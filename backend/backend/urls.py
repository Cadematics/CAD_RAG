from django.contrib import admin
from django.urls import path
from rag.views import query_rag, health, chunk_detail


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/query/", query_rag),
    path("api/chunks/<uuid:chunk_id>/", chunk_detail),
]
