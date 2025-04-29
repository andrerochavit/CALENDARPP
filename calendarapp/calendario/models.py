from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    class Meta:
        abstract = True

class Aluno(PerfilUsuario):
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    semestre = models.IntegerField()

class Professor(PerfilUsuario):
    departamento = models.CharField(max_length=100)
    titulo = models.CharField(max_length=50)  # ex: Dr., Me., etc

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    coordenador = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    periodo = models.IntegerField()  # semestre/período em que a matéria é ministrada
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Post(models.Model):
    TIPO_CHOICES = [
        ('EVENTO', 'Evento'),
        ('PROJETO', 'Projeto'),
        ('AVISO', 'Aviso'),
    ]
    
    VISIBILIDADE_CHOICES = [
        ('PUBLICO', 'Público'),
        ('CURSO', 'Específico para Curso'),
        ('MATERIA', 'Específico para Matéria'),
    ]
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    visibilidade = models.CharField(max_length=20, choices=VISIBILIDADE_CHOICES, default='PUBLICO')
    
    # Relacionamentos
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True, blank=True)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, null=True, blank=True)
    
    # Campos temporais
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_evento = models.DateTimeField(null=True, blank=True)
    local = models.CharField(max_length=200, null=True, blank=True)
    
    # Participantes
    participantes = models.ManyToManyField(User, related_name='eventos_participando', blank=True)
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post, related_name='tags')
