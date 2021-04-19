from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
import re

from ..models.item import Item
from ..models.material import Material
from ..serializers import ItemSerializer, UserSerializer, ItemGetSerializer

# Create your views here.
class Items(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ItemSerializer
    def get(self, request):
        """Index request"""
        # Get all the items:
        # items = Data.objects.all()
        # Filter the items by owner, so you can only see your owned items
        print(request.user, "request user")
        items = Item.objects.all()
        # Run the data through the serializer
        data = ItemGetSerializer(items, many=True).data
        print(data, "the data")
        return Response({ 'items': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        # request.POST = request.POST.copy()
        request.data['owner'] = request.user.id
        print(request.data, "request")
        # Serialize/create item
        item = ItemSerializer(data=request.data)
        # If the item data is valid according to our serializer...
        if item.is_valid():
            print(item, "item after serializer", item.is_valid())
            # Save the created item & send a response
            item.save()
            return Response({ 'item': item.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        print(item.errors, "item errors")
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete request"""
        # Locate item to delete
        item = get_object_or_404(Item, pk=pk)
        # Check the item's owner agains the user making this request
        if not request.user.id == item.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this item')
        # Only delete if the user owns the  item
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemGetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the item to show
        print("my request:", request,  "my request", pk)

        item = get_object_or_404(Item, pk=pk)

        print(item)

        data = ItemGetSerializer(item).data
        print(data, "my data")
        return Response({ 'items': [data] }, status=status.HTTP_201_CREATED)



class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, slug):
        """Show request"""
        # Locate the item to show

        item = Item.objects.filter(barcode=slug)
        # print("my request:", item[0],  "my request", slug)

        # if 'Material' in item[0].description:
        #     mystring = item[0].description
        #     after_keyword = mystring.partition('Material: -')
        #     mat_keyword = after_keyword[2].split()[0]
        #     print(mat_keyword, "my material")
        #     mat = Material.objects.filter(name=mat_keyword)
        #     if mat:
        #         print(mat[0].recycleable)
        #         item[0].recycleable = mat[0].recycleable
        #     else:
        #         item[0].recycleable

        # //print(x)
        if not item:
            print("item was empty")
            item = get_object_or_404(Item, name=slug)
            data = ItemGetSerializer(item).data
            print(data, "my data")
            return Response({ 'items': [data] }, status=status.HTTP_201_CREATED)

        data = ItemGetSerializer(item[0]).data
        print(data, "my data")
        return Response({ 'items': [data] }, status=status.HTTP_201_CREATED)


    def delete(self, request, pk):
        """Delete request"""
        # Locate item to delete
        item = get_object_or_404(Item, pk=pk)
        # Check the item's owner agains the user making this request
        if not request.user.id == item.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this item')
        # Only delete if the user owns the  item
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['item'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        p_k = request.data['id']
        if request.data.get('owner', False):
            del request.data['owner']

        # Locate Item
        # get_object_or_404 returns a object representation of our Item
        item = get_object_or_404(Item, pk=p_k)
        material = get_object_or_404(Material, name=request.data['material'])
        request.data['material'] = material.id
        # Check if user is the same as the request.user.id
        if not request.user.is_superuser or not request.user.id == item.owner.id :
            raise PermissionDenied('Unauthorized, you do not own this item')

        # Add owner to data object now that we know this user owns the resource
        request.data['owner'] = request.user.id

        if not request.data['owner']:
            print("no")
        # Validate updates with serializer
        data = ItemSerializer(item, data=request.data, partial=True)

        if data.is_valid():
            # Save & send a 204 no content
            print(data, "is valid")
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        print(data.errors)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
