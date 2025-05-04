from django.urls import path
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamingPlatformListAV, StreamingPlatformDetailAV

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="watch_list"),
    path("<int:pk>", WatchDetailAV.as_view(), name="detail"),
    path("platform/", StreamingPlatformListAV.as_view(), name="platform_list"),
    path("platform/<int:pk>", StreamingPlatformDetailAV.as_view(), name="platform_detail"),
]
