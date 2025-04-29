from django.contrib import admin
from .models import Aluno, Professor, Curso, Materia,  Post, Comentario, Tag

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Tag)
