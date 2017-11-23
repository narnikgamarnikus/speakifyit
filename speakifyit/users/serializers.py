'''
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
'''

from rest_framework import serializers
from django.conf import settings

from .models import User, Language, LanguageSkill
from annoying.functions import get_object_or_None


class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Language
        fields = ('language')


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = LanguageSkill
        fields = ('language', 'skill')


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)

    avatar_url = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    native = serializers.SerializerMethodField(read_only=True)
    learn = serializers.SerializerMethodField(read_only=True)

    def get_native(self, obj):
        if obj:
            language = get_object_or_None(LanguageSkill, language=obj.native, user=obj)
            if language:
                return {
                    'language': language.language.language,
                    'skill': language.skill
                    }
    
    def get_learn(self, obj):
        if obj:
            languages = [get_object_or_None(LanguageSkill, user=obj, language=language) for language in obj.learn.all()]
            return [{'language': language.language.language, 'skill': language.skill} for language in languages if language is not None ]

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else settings.STATIC_URL + 'images/default_avatar.png'

    def get_short_name(self, obj):
        return obj.short_name

    def get_full_name(self, obj):
        return obj.full_name

    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_active',
                   'groups', 'user_permissions', 'first_name',
                   'last_name', 'middle_name']


class UserWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['is_active']
