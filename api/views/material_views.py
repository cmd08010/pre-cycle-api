from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.material import Material
from ..serializers import MaterialSerializer

class Materials(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = MaterialSerializer
    def get(self, request):
        """Index request"""
        materials = Material.objects.all()
        # Run the data through the serializer
        data = MaterialSerializer(materials, many=True).data
        print(data, "the data")
        return Response({ 'materials': data })

    def post(self, request):
        """Create request"""
        material = MaterialSerializer(data=request.data)
        # If the item data is valid according to our serializer...
        if material.is_valid():
            print(material, "material after serializer", material.is_valid())
            # Save the created material & send a response
            material.save()
            return Response({ 'material': material.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        print(material.errors, "material errors")
        return Response(material.errors, status=status.HTTP_400_BAD_REQUEST)
