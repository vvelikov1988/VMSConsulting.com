from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_pic']

    def get_profile_pic(self, obj):
        return obj.profile_pic.thumbnail.url
