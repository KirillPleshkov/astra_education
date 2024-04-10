from rest_framework import serializers

from curriculum.models import Curriculum, CurriculumDiscipline, CurriculumDisciplineUser, EducationalLevel
from discipline.api.serializers import DisciplineSerializer, DisciplineNameSerializer
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
    discipline = DisciplineNameSerializer()

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


class CurriculumNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ('id', 'name')
