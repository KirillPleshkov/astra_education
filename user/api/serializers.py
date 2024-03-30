from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import LinguistsRoles


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    linguist_roles = serializers.SerializerMethodField()

    def get_role(self, obj):
        return get_user_model().Roles(obj.role).label, get_user_model().Roles(obj.role).name

    def get_linguist_roles(self, obj):
        return [(LinguistsRoles.LinguistsRolesChose(role.linguist_role).label,
                 LinguistsRoles.LinguistsRolesChose(role.linguist_role).name) for role in obj.linguist_roles.all()]

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'role', 'linguist_roles', 'curriculum')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name')
