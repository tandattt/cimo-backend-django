from rest_framework import serializers
from Blogs.models import SoBlogs

class SoBlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoBlogs
        fields = '__all__'
