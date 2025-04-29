from rest_framework import viewsets, generics, permissions
from .models import Post, Comentario, User, Aluno, Professor, Materia, Curso
from .serializers import PostSerializer, ComentarioSerializer, UserCreateSerializer, AlunoSerializer, ProfessorSerializer, CursoSerializer

from django.db.models.functions import TruncDate
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(visibilidade='PUBLICO')

        if user.is_authenticated:
            try:
                aluno = Aluno.objects.get(user=user)
                curso = aluno.curso
                curso_posts = Post.objects.filter(visibilidade='CURSO', curso=curso)
                materia_posts = Post.objects.filter(
                    visibilidade='MATERIA',
                    materia__curso=curso
                )
                queryset = queryset.union(curso_posts, materia_posts)

            except Aluno.DoesNotExist:
                try:
                    professor = Professor.objects.get(user=user)
                    cursos = Curso.objects.filter(coordenador=professor)
                    materias = Materia.objects.filter(professor=professor)
                    curso_posts = Post.objects.filter(visibilidade='CURSO', curso__in=cursos)
                    materia_posts = Post.objects.filter(visibilidade='MATERIA', materia__in=materias)
                    queryset = queryset.union(curso_posts, materia_posts)
                except Professor.DoesNotExist:
                    pass

        return queryset.order_by('-data_criacao')

    def perform_create(self, serializer):
        curso = self.request.data.get('curso')
        materia = self.request.data.get('materia')

        if materia:
            visibilidade = 'MATERIA'
        elif curso:
            visibilidade = 'CURSO'
        else:
            visibilidade = 'PUBLICO'

        serializer.save(autor=self.request.user, visibilidade=visibilidade)

    @action(detail=False, methods=['get'])
    def por_dia(self, request):
        posts_por_dia = Post.objects.annotate(data=TruncDate('data_criacao')) \
            .values('data') \
            .annotate(total=Count('id')) \
            .order_by('-data')
        return Response(posts_por_dia)

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
