from rest_framework import serializers
from family.models import user, family, package

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ["username", "password", "firstname", "lastname", "phone_number", "gender"]

    def create(self, validated_data):
            usr = user.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
            )
            usr.firstname = validated_data['firstname']
            usr.lastname = validated_data['lastname']
            usr.gender = validated_data['gender']
            usr.phone_number = validated_data['phone_number']
            usr.save()
            return usr

    
class UserSerializer1(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=100)
    firstname = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=16)
    gender = serializers.CharField(max_length=1)

    def create(self, validated_data):
        return user.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance    



class CreateFamilySerializer(serializers.Serializer):
    parents_username = serializers.ListField()
    childs_username = serializers.ListField(required=False)


class PackageSelectionSerializer(serializers.Serializer):
    child_username = serializers.CharField(max_length=30, required=True)
    package_type = serializers.CharField(max_length=20, required=True)


class PackageDeletionSerializer(serializers.Serializer):
    child_username = serializers.CharField(max_length=30, required=True)
