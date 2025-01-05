from rest_framework import serializers

from users.models import Users


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    active = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Users
        fields = [
            'document_type',
            'document_number',
            'name',
            'last_name',
            'age',
            'email',
            'active',
            'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
