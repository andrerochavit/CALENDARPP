from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Professor, Curso, Materia, Post, Comentario, Tag

# Serializer para User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializer para Aluno
class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Aluno
        fields = '__all__'

# Serializer para Professor
class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Professor
        fields = '__all__'

# Serializer para Curso
class CursoSerializer(serializers.ModelSerializer):
    coordenador = ProfessorSerializer(read_only=True)
    
    class Meta:
        model = Curso
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)
    
    class Meta:
        model = Materia
        fields = '__all__'

# Serializer para Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# Serializer para Comentário
class ComentarioSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)
    
    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ('data_criacao',)

# Serializer para Post
class PostSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    participantes = UserSerializer(many=True, read_only=True)
    curso = CursoSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('data_criacao',)

    def validate(self, data):
        """
        Valida se os campos curso e materia estão consistentes com a visibilidade escolhida
        """
        visibilidade = data.get('visibilidade')
        curso = data.get('curso')
        materia = data.get('materia')

        if visibilidade == 'CURSO' and not curso:
            raise serializers.ValidationError("Para posts específicos de curso, é necessário especificar um curso")
        
        if visibilidade == 'MATERIA' and not materia:
            raise serializers.ValidationError("Para posts específicos de matéria, é necessário especificar uma matéria")

        return data