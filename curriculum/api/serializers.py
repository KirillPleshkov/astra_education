from django.contrib.auth import get_user_model
from rest_framework import serializers

from curriculum.models import Curriculum, CurriculumDiscipline, CurriculumDisciplineUser, EducationalLevel
from discipline.api.serializers import DisciplineSerializer, DisciplineNameSerializer, ElementSerializer
from discipline.models import Discipline
from user.api.serializers import UserSerializer, TeacherSerializer


class EducationalLevelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    study_period = serializers.IntegerField(read_only=True)


class CurriculumDisciplineUserSerializer(serializers.ModelSerializer):
    user = TeacherSerializer()

    class Meta:
        model = CurriculumDisciplineUser
        fields = ('user',)


class CurriculumDisciplineSerializer(serializers.ModelSerializer):
    teachers = CurriculumDisciplineUserSerializer(many=True, source='curriculumdisciplineuser_set')
    discipline = ElementSerializer()

    class Meta:
        model = CurriculumDiscipline
        fields = ('teachers', 'discipline', 'semester')


class CurriculumSerializer(serializers.ModelSerializer):
    disciplines = CurriculumDisciplineSerializer(many=True, source='curriculumdiscipline_set')
    educational_level = EducationalLevelSerializer()

    class Meta:
        model = Curriculum
        fields = ('id', 'name', 'disciplines', 'educational_level')

    def create(self, validated_data):
        educational_level_name = validated_data.pop('educational_level').get('name')
        educational_level = EducationalLevel.objects.get(name=educational_level_name)
        return Curriculum.objects.create(name=validated_data.pop('name'), educational_level=educational_level)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        educational_level_name = validated_data.pop('educational_level').get('name')
        educational_level = EducationalLevel.objects.get(name=educational_level_name)
        instance.educational_level = educational_level

        CurriculumDiscipline.objects.filter(curriculum=instance).delete()

        for discipline in validated_data.pop('curriculumdiscipline_set'):
            discipline_object = Discipline.objects.get(id=discipline.get('discipline').get('id'))
            obj = CurriculumDiscipline.objects.create(semester=discipline.get('semester'), discipline=discipline_object,
                                                      curriculum=instance)

            for user in discipline.get('curriculumdisciplineuser_set'):
                user_obj = get_user_model().objects.get(first_name=user.get('user').get('first_name'),
                                                        last_name=user.get('user').get('last_name'))
                CurriculumDisciplineUser.objects.create(user=user_obj, curriculum_discipline=obj)

        instance.save()

        return instance


class CurriculumNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ('id', 'name')
