from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

# displays all data i.e the profiles created which link to the users in a JSON format
# Displays all profile data linked to the users in a JSON format
class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context ={'request': request})
        return Response(serializer.data)
    

class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # gets the profile object specifially by the id and on returns that results
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
         # gets the profile object specifially by the id and on returns that results and convert it to JSON before displaying it
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context ={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Gets the profile object specifically by the id and updates it with the data provided in the request
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context ={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)