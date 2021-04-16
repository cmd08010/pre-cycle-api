from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.item import Item
from ..serializers import ItemSerializer, UserSerializer

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
        data = ItemSerializer(items, many=True).data
        print(data, "the data")
        return Response({ 'items': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        print(request.data, "request")
        # request.POST = request.POST.copy()
        request.data['owner'] = request.user.id
        # Serialize/create item
        item = ItemSerializer(data=request.data)
        print(item, "item after serializer")
        # If the item data is valid according to our serializer...
        if item.is_valid():
            # Save the created item & send a response
            item.save()
            return Response({ 'item': item.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        print(item.errors, "item errors")
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the item to show
        item = get_object_or_404(Item, pk=pk)
        # Only want to show owned items?
        if not request.user.id == item.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this item')

        # Run the data through the serializer so it's formatted
        data = ItemSerializer(item).data
        return Response({ 'item': data })

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

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['item'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['item'].get('owner', False):
            del request.data['item']['owner']

        # Locate Item
        # get_object_or_404 returns a object representation of our Item
        item = get_object_or_404(Item, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == item.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this item')

        # Add owner to data object now that we know this user owns the resource
        request.data['item']['owner'] = request.user.id
        # Validate updates with serializer
        data = ItemSerializer(item, data=request.data['item'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
