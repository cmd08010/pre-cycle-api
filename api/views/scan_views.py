import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
import requests
from dotenv import load_dotenv, find_dotenv

from ..models.scan import Scan
from ..models.user import User
from ..models.item import Item
from ..serializers import ScanSerializer, UserSerializer, ItemSerializer, ScanGetSerializer, ItemGetSerializer

# Create your views here.
class Scans(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ScanSerializer
    def get(self, request):
        """get all scans for super user or just owner'sscans if not superuser"""
        print(request.user.is_superuser, "request")

        scans = Scan.objects.filter(owner=request.user.id)
        if scans :
            print(scans, "my scans")
            data = ScanGetSerializer(scans, many=True).data

        if request.user.is_superuser:
            all_scans = Scan.objects.all()
            if all_scans :
                all_data = ScanGetSerializer(all_scans, many=True).data

            return Response({ 'scans': data, "all-scans": all_data})

        else:
            return Response({ 'scans': data })


    def post(self, request):
        """Create request"""
        # Add user to request data object
        print(request.user, "request")
        # request.POST = request.POST.copy()
        request.data[0]['owner'] = request.user.id
        # # Serialize/create item
        scan = ScanSerializer(data=request.data[0])
        print(scan, "scan after serializer")
        # # If the scan data is valid according to our serializer...
        if scan.is_valid():
            scan.save()
            return Response({ 'scan': scan.data }, status=status.HTTP_201_CREATED)
        # # If the data is not valid, return a response with the errors
        # print(scan.errors, "scan errors")
        return Response("scan.errors", status=status.HTTP_400_BAD_REQUEST)
            # return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        # If the data is not valid, return a response with the errors

class ScanDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, slug):
        """Show request"""
        # Locate the scan to show
        print(slug, "pk", request.get_full_path)
        scan = Item.objects.filter(name=slug)
        print(scan)
        if not scan:
            scan = Item.objects.filter(barcode=slug)
            print(scan)
            # scan = get_object_or_404(Scan, )
        # # Only want to show owned scans?
        # if not request.user.id == scan[0].owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this scan')

        data = ItemGetSerializer(scan[0]).data
        print(data)
        return Response({ 'items': [data] })

        # # Run the data through the serializer so it's formatted

    def delete(self, request, pk):
        """Delete request"""
        # Locate scan to delete
        scan = get_object_or_404(Scan, pk=pk)
        print(scan, "super", request.user.is_superuser)
        # Check the scan's owner agains the user making this request
        if request.user.is_superuser or request.user.id == scan.owner.id:
            scan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Only delete if the user owns the  scan
        else:
            print(request.user.is_superuser)
            raise PermissionDenied('Unauthorized, you do not own this scan')

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


class ScanApiDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, slug):
        """Show request"""
        load_dotenv(find_dotenv())
        api_key = os.environ.get("API_KEY")

        # Locate the scan to show
        response = requests.get(f"https://api.barcodelookup.com/v2/products?barcode={slug}&formatted=y&key={api_key}")
        print(response)
        if response:
            item = response.json()
            if item:
                print(item)
                return Response({'item': item}, status=status.HTTP_200_OK)
        else:
            errors = "No item found"

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
