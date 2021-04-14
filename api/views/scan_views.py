from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.scan import Scan
from ..serializers import ScanSerializer, UserSerializer

# Create your views here.
class Scans(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ScanSerializer
    def get(self, request):
        """Index request"""
        # Get all the scans:
        # scans = Scan.objects.all()
        # Filter the scans by owner, so you can only see your owned scans
        print(request.user, "request user")
        scans = Scan.objects.filter(owner=request.user.id)
        print(scans, "the scans")
        # Run the data through the serializer
        data = ScanSerializer(scans, many=True).data
        return Response({ 'scans': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        print(request.data, "request")
        request.data['owner'] = request.user.id
        # Serialize/create scan
        scan = ScanSerializer(data=request.data)
        # If the scan data is valid according to our serializer...
        if scan.is_valid():
            # Save the created scan & send a response
            scan.save()
            return Response({ 'scan': scan.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        print(scan.errors, "scan errors")
        return Response(scan.errors, status=status.HTTP_400_BAD_REQUEST)

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
