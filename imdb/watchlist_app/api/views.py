from rest_framework.request import Request
from rest_framework.response import Response

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.api.serializers import WatchListSerializer, StreamingPlatformSerializer
from watchlist_app.models import WatchList, StreamingPlatform
from rest_framework import status


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


class StreamingPlatformListAV(APIView):

    def get(self, request: Request):
        platform = StreamingPlatform.objects.all()
        serailizer = StreamingPlatformSerializer(
            platform,
            many=True,
            context={"request": request},
        )
        return Response(serailizer.data)

    def post(self, request: Request):
        serailizer = StreamingPlatformSerializer(data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors)


class StreamingPlatformDetailAV(APIView):
    def get(self, request: Request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serailizer = StreamingPlatformSerializer(platform)
        return Response(serailizer.data)

    def put(self, request: Request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serailizer = StreamingPlatformSerializer(platform, data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        if platform is None:
            return Response(status=404)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
