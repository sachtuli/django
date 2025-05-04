from django.shortcuts import get_object_or_404
from rest_framework import status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics, viewsets

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly

# from rest_framework.decorators import api_view
from watchlist_app.api.serializers import WatchListSerializer, StreamingPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamingPlatform, Review


class WatchListAV(APIView):
    def get(self, request: Request):
        movie = WatchList.objects.all()
        serailizer = WatchListSerializer(movie, many=True)
        return Response(serailizer.data)

    def post(self, request: Request):
        serailizer = WatchListSerializer(data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors)


class WatchDetailAV(APIView):
    def get(self, request: Request, pk):
        movie = WatchList.objects.get(pk=pk)
        serailizer = WatchListSerializer(movie)
        return Response(serailizer.data)

    def put(self, request: Request, pk):
        movie = WatchList.objects.get(pk=pk)
        serailizer = WatchListSerializer(movie, data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors)

    def delete(self, request: Request, pk):
        movie = WatchList.objects.get(pk=pk)
        if movie is None:
            return Response(status=404)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformMVS(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer


# class StreamPlatformVS(viewsets.ViewSet):
# def list(self, request: Request):
#     queryset = StreamingPlatform.objects.all()
#     serailizer = StreamingPlatformSerializer(queryset, many=True)
#     return Response(serailizer.data)

# def retrieve(self, request: Request, pk=None):
#     queryset = StreamingPlatform.objects.get(pk=pk)
#     watchlist = get_object_or_404(queryset)
#     serailizer = StreamingPlatformSerializer(watchlist)
#     return Response(serailizer.data)

# def create(self, request: Request):
#     serailizer = StreamingPlatformSerializer(data=request.data)
#     if serailizer.is_valid():
#         serailizer.save()
#         return Response(serailizer.data)
#     return Response(serailizer.errors)


# class StreamingPlatformListAV(APIView):

#     def get(self, request: Request):
#         platform = StreamingPlatform.objects.all()
#         serailizer = StreamingPlatformSerializer(
#             platform,
#             many=True,
#             context={"request": request},
#         )
#         return Response(serailizer.data)

#     def post(self, request: Request):
#         serailizer = StreamingPlatformSerializer(data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data)
#         return Response(serailizer.errors)


# class StreamingPlatformDetailAV(APIView):
#     def get(self, request: Request, pk):
#         platform = StreamingPlatform.objects.get(pk=pk)
#         serailizer = StreamingPlatformSerializer(platform)
#         return Response(serailizer.data)

#     def put(self, request: Request, pk):
#         platform = StreamingPlatform.objects.get(pk=pk)
#         serailizer = StreamingPlatformSerializer(platform, data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data)
#         return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request: Request, pk):
#         platform = StreamingPlatform.objects.get(pk=pk)
#         if platform is None:
#             return Response(status=404)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Using Generic Concrete View Classes
class ReviewList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(Watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        movie = WatchList.objects.get(pk=pk)
        reviewee = self.request.user
        review_qs = Review.objects.filter(Watchlist=movie, review_user=reviewee)

        if review_qs.exists():
            raise exceptions.ValidationError("You have already reviewed this movie!")

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data["review"]
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data["review"]) / 2

        movie.number_rating += 1
        movie.save()
        serializer.save(Watchlist=movie, review_user=reviewee)


# # Using Mixins
# class ReviewDetail(mixins.RetrieveModelMixin, GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# @api_view(["GET", "POST"])
# def movie_list(request: Request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serailizer = MovieSerializer(movies, many=True)
#         return Response(serailizer.data)

#     if request.method == "POST":
#         serailizer = MovieSerializer(data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data)
#         return Response(serailizer.errors)


# @api_view(["GET", "PUT", "DELETE"])
# def movie_detail(request, pk):
#     if request.method == "GET":
#         movie = Movie.objects.get(pk=pk)
#         serailizer = MovieSerializer(movie)
#         return Response(serailizer.data)

#     if request.method == "DELETE":
#         movie = Movie.objects.get(pk=pk)
#         if movie is None:
#             return Response(status=404)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     if request.method == "PUT":
#         movie = Movie.objects.get(pk=pk)
#         serailizer = MovieSerializer(movie, data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data)
#         return Response(serailizer.errors)
