from rest_framework import serializers
from.models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the post model
    """
    date_created = serializers.ReadOnlyField()

    class Meta(object):
        model = Post
        fields = ('article', 'author', 'title', 'title_url', 'summary', 'content', 'views', 'rate', 'date_created')
