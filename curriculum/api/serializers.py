from rest_framework import serializers

from curriculum.models import Curriculum, CurriculumDiscipline, CurriculumDisciplineUser, EducationalLevel
from discipline.api.serializers import DisciplineSerializer, DisciplineNameSerializer
from user.api.serializers import UserSerializer, TeacherSerializer


class EducationalLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalLevel
        fields = '__all__'


class CurriculumDisciplineUserSerializer(serializers.ModelSerializer):
    user = TeacherSerializer(read_only=True)

    class Meta:
        model = CurriculumDisciplineUser
        fields = ('user',)


class CurriculumDisciplineSerializer(serializers.ModelSerializer):
    teachers = CurriculumDisciplineUserSerializer(many=True, read_only=True, source='curriculumdisciplineuser_set')
    discipline = DisciplineNameSerializer(read_only=True)

    class Meta:
        model = CurriculumDiscipline
        fields = ('teachers', 'discipline', 'semester')


class CurriculumSerializer(serializers.ModelSerializer):
    disciplines = CurriculumDisciplineSerializer(many=True, read_only=True, source='curriculumdiscipline_set')
    educational_level = EducationalLevelSerializer(read_only=True)

    class Meta:
        model = Curriculum
        fields = ('id', 'name', 'disciplines', 'educational_level')
