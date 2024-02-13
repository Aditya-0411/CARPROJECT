from rest_framework_simplejwt.tokens import RefreshToken

from cars.models import Cars
from cars.models import Like, Comments
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarsSerializer, LikeSerializer , CommentSerializer, RegisterSerializer,LoginSerializer,UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            print(f"User {user.username} registered successfully!")
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve username and password from the validated data
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user:
                # Login the user
                login(request, user)

                # Generate tokens
                refresh = RefreshToken.for_user(user)

                # Return the response
                return Response({
                    "status": "success",
                    "data": {
                        "user": UserSerializer(user).data,
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh)
                    }
                }, status=status.HTTP_200_OK)

            # If authentication fails
            return Response({"status": "error", "data": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # If serializer validation fails
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CarsViewset(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self, request, id=None):
    #     if id:
    #         item = models.Cars.objects.get(id=id)
    #         serializer = serializers.CarsSerializer(item)
    #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    #
    #     items = models.Cars.objects.all()
    #
    #     serializer = serializers.CarsSerializer(items, many=True)
    #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

#get code to see the cars and likes
    def get(self, request):
        items = Cars.objects.all()

        # Add the 'liked' and 'likes' fields to each car in the queryset
        cars_data = []
        for car in items:
            liked = self.get_like_status(request.user, car)
            serializer = CarsSerializer(car)
            data = serializer.data
            data['liked'] = liked
            data['likes'] = car.likes
            cars_data.append(data)

        return Response({"status": "success", "data": cars_data}, status=status.HTTP_200_OK)

    def get_like_status(self, user, car):
        """
        Check if the user has liked the given car.
        """
        if user.is_authenticated:
            return Like.objects.filter(user=user, car=car).exists()
        return False

# #to see comments
    def get(self, request):
        cars = Cars.objects.annotate(comment_count=Count('comments'))  # Count the number of comments for each car
        serializer = serializers.CarsSerializer(cars, many=True)

        # Customize the serializer to include comment information
        serialized_data = serializer.data
        for i, car_data in enumerate(serialized_data):
            car_id = car_data['id']
            comments = Comments.objects.filter(car_id=car_id)
            comment_serializer = CommentSerializer(comments, many=True)
            serialized_data[i]['comments'] = comment_serializer.data

        return Response({"status": "success", "data": serialized_data}, status=status.HTTP_200_OK)



    def post(self, request):
        serializer = serializers.CarsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            cars = models.Cars.objects.get(id=id)
            serializer = CarsSerializer(cars, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data})
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except models.Cars.DoesNotExist:
            return Response({"status": "error", "data": "Cars object not found"}, status=status.HTTP_404_NOT_FOUND)

    # def delete(self, request):
    #     item = models.Cars.objects.filter(id=request.data["id"])
    #     print(item)
    #     item.delete()
    #     return Response({"status": "success", "data": "Item Deleted"})

    def delete(self, request):
        try:
            item = models.Cars.objects.filter(id=request.data["id"])
            print(item)
            item.delete()
            return Response({"status": "success", "data": "Item Deleted"})
        except Exception as e:
            print(f"Error: {e}")
            return Response({"status": "error", "data": "An error occurred"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#FOR LIKE MODEL:
class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
          print(request.user)
          car = get_object_or_404(Cars, id=id)
          like_data = {'user': request.user.id, 'car': car.id}
          like_serializer = LikeSerializer(data=like_data)

          if like_serializer.is_valid():
             like_serializer.save()
             return Response({"status": "success", "data": "Car liked"}, status=status.HTTP_200_OK)
          else:
             return Response({"status": "error", "data": like_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
            car = get_object_or_404(Cars, id=id)
            like = Like.objects.filter(user=request.user, car=car).first()

            if like:
                like.delete()
                return Response({"status": "success", "data": "Like removed"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": "No like found"}, status=status.HTTP_404_NOT_FOUND)



class CommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, comment_id=None):
        if comment_id is not None:
            # Retrieve a specific comment
            comment = get_object_or_404(Comments, id=comment_id)
            serializer = CommentSerializer(comment)
        else:
            # List all comments
            comments = Comments.objects.all()
            serializer = CommentSerializer(comments, many=True)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, *comment_id, **kwargs):
    #     print(kwargs)
    #     # Delete an existing comment
    #     comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    #     comment.delete()
    #     return Response({"status": "success", "data": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)


    # def put(self, request, comment_id):
    #     comment = get_object_or_404(Comments, id=comment_id)
    #     serializer = CommentSerializer(comment, data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id=None):
            try:
                # Retrieve the specific comment
                comment = get_object_or_404(Comments, id=id, user=request.user)

                # Delete the comment
                comment.delete()

                return Response({"status": "success", "data": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)

            except Comments.DoesNotExist:
                return Response({"status": "error", "data": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "data": f"An error occurred: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


