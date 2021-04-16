from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.scan import Scan
from ..models.item import Item
from ..serializers import ScanSerializer, UserSerializer, ItemSerializer

# Create your views here.
class Scans(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ScanSerializer
    def get(self, request):
        """Index request"""
        scans = Scan.objects.filter(owner=request.user.id)
        if scans :
            print(scans, "my scans")
            data = ScanSerializer(scans, many=True).data
            return Response({ 'scans': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        print(request.data, "request")
        print("my request:", request,  "my request", request.data)
        items = Item.objects.filter(name=request.data['name'])
        print(items)
        if items :
            print(items, "the items")
            data = ItemSerializer(items, many=True).data
            return Response({ 'items': data }, status=status.HTTP_201_CREATED)
        else:
            scans = Scan.objects.filter(name=request.data)
            print(scans, "the scans")
            # Run the data through the serializer
            data = ScanSerializer(scans, many=True).data
            return Response({ 'scans': data })
            # return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        # If the data is not valid, return a response with the errors

class ScanDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the scan to show
        scan = get_object_or_404(Scan, pk=pk)
        # Only want to show owned scans?
        if not request.user.id == scan.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this scan')

        # Run the data through the serializer so it's formatted
        data = ScanSerializer(scan).data
        return Response({ 'scan': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate scan to delete
        scan = get_object_or_404(Scan, pk=pk)
        # Check the scan's owner agains the user making this request
        if not request.user.id == scan.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this scan')
        # Only delete if the user owns the  scan
        scan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['scan'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['scan'].get('owner', False):
            del request.data['scan']['owner']

        # Locate Scan
        # get_object_or_404 returns a object representation of our Scan
        scan = get_object_or_404(Scan, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == scan.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this scan')

        # Add owner to data object now that we know this user owns the resource
        request.data['scan']['owner'] = request.user.id
        # Validate updates with serializer
        data = ScanSerializer(scan, data=request.data['scan'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
