from .models import Image
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    detected_image = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Image
        fields = ['id','image','detected_image']
