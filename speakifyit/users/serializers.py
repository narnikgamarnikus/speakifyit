from rest_framework import serializers
from .models import User, Language


class LanguageSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Language
		fields = ('id', 'language', 'flag')


class UserSerializer(serializers.ModelSerializer):
	native = LanguageSerializer(many=True)
	learn = LanguageSerializer(many=True)

	class Meta:
		model = User
		fields = ('id', 'name', 'username', 'native', 'learn')