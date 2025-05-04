from django.urls import path, include
from rest_framework import routers
from watchlist_app.api.views import (
    WatchListAV,
    WatchDetailAV,
    StreamPlatformMVS,
    # StreamPlatformVS,
    # StreamingPlatformListAV,
    # StreamingPlatformDetailAV,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
)

router = routers.DefaultRouter()
router.register("stream", StreamPlatformMVS, basename="streamplatform")

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="watch_list"),
    path("<int:pk>/", WatchDetailAV.as_view(), name="detail"),
    # path("stream/", StreamingPlatformListAV.as_view(), name="stream-list"),
    # path("stream/<int:pk>", StreamingPlatformDetailAV.as_view(), name="stream-detail"),
    path("", include(router.urls)),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]
