from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.contrib import admin

from ..serializers import UserSerializer, UserRegisterSerializer, ChangePasswordSerializer, UsersSerializer, ChangeUserActiveSerializer
from ..models.user import User

class SignUp(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    # Serializer classes are required for endpoints that create data
    serializer_class = UserRegisterSerializer

    def post(self, request):
        # Pass the request data to the serializer to validate it
        user = UserRegisterSerializer(data=request.data['credentials'])
        # If that data is in the correct format...
        if user.is_valid():
            # Actually create the user using the UserSerializer (the `create` method defined there)
            created_user = UserSerializer(data=user.data)
            if created_user.is_valid():
                # Save the user and send back a response!
                created_user.save()
                print(created_user.data, "create-user-data")
                return Response({ 'user': created_user.data }, status=status.HTTP_201_CREATED)
            else:
                print(created_user.errors, "created errors")
                return Response(created_user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(user.errors[0], "errors")
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()

    # Serializer classes are required for endpoints that create data
    serializer_class = UserSerializer

    def post(self, request):
        creds = request.data['credentials']
        print(creds, "creds")
        # We can pass our email and password along with the request to the
        # `authenticate` method. If we had used the default user, we would need
        # to send the `username` instead of `email`.
        user = authenticate(request, email=creds['email'], password=creds['password'])
        # Is our user is successfully authenticated...
        if user is not None:
            # And they're active...
            if user.is_active:
                # Log them in!
                login(request, user)
                # Finally, return a response with the user's token
                return Response({
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'token': user.get_auth_token(),
                        'is_superuser': user.is_superuser,
                        'is_active': user.is_active
                    }
                })
            else:
                return Response({ 'msg': 'The account is inactive.' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'msg': 'The username and/or password is incorrect.' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class SignOut(generics.DestroyAPIView):
    def delete(self, request):
        # Remove this token from the user
        request.user.delete_token()
        # Logout will remove all session data
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePassword(generics.UpdateAPIView):
    def partial_update(self, request):
        user = request.user
        # Pass data through serializer
        serializer = ChangePasswordSerializer(data=request.data['passwords'])
        if serializer.is_valid():
            # This is included with the Django base user model
            # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.check_password
            if not user.check_password(serializer.data['old']):
                return Response({ 'msg': 'Wrong password' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # set_password will also hash the password
            # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.set_password
            user.set_password(serializer.data['new'])
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Admin(generics.ListCreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    permission_classes = (IsAuthenticated,)

    # Serializer classes are required for endpoints that create data
    serializer_class = UsersSerializer
    def get(self, request):
        """Get all the users for the admin"""
        # Locate the scan to show

        get_users = User.objects.all().order_by('id')
        # Only want to show owned scans?
        if not request.user.is_superuser:
            raise PermissionDenied('Unauthorized, you are not an admin')

        # Run the data through the serializer so it's formatted
        users = UsersSerializer(get_users, many=True).data
        return Response({ 'users': users })

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Get One users for the admin request"""
        # Locate the scan to show
        user = get_object_or_404(User, pk=pk)
        # Only want to show owned users?
        if not request.user.is_superuser:
            raise PermissionDenied('Unauthorized, you are not an admin')

        # Run the data through the serializer so it's formatted
        data = User(user).data
        return Response({ 'user': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate user to delete
        user = get_object_or_404(User, pk=pk)
        # Check the user's owner agains the user making this request
        if not request.user.id == user.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this user')
        # Only delete if the user owns the  user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        """Update the is_active section for the User"""
        # Remove owner from request object
        # This "gets" the owner key on the data['user'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.user.is_superuser:
            user = get_object_or_404(User, pk=pk)
            serializer = ChangeUserActiveSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(user, request.data)
                user.save()
                print(serializer)
        # else:
                return Response(status=status.HTTP_204_NO_CONTENT)
            # return Response("You are not an admin", status=status.HTTP_400_BAD_REQUEST)
