from rest_framework import serializers

from blog_api.models import Bannedwords


class bannedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bannedwords
        fields = '__all__'