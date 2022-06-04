from rest_framework import serializers
from.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model
    """
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id','email', 'username', 'date_joined', 'password', 'posts_info')

        extra_kwargs = {'password':{'write_only':True}}