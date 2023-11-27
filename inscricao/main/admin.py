from django.contrib import admin
from .models import *


class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('codigo_estudante', 'nome', 'apelido', 'sexo', 'celular', 'nascimento', 'curso', 'email','ano_ingresso')
    list_editable=('nome', 'apelido','celular','curso', 'email')


class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class CadeiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'horas', 'semestre', 'ano')

class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'codigo_estudante', 'cadeira', 'data_inscricao', 'feito')  # Adicionado 'codigo_estudante'
    list_filter = ('cadeira__semestre', 'codigo_estudante')  # Adicionado 'codigo_estudante' aos filtros
    search_fields = ('estudante__codigo_estudante', 'codigo_estudante')  # Adicionado 'codigo_estudante' para pesquisa


    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cadeira":
            # Obtenha o semestre ativo a partir das configurações
            configuracoes = Configuracoes.objects.first()
            semestre_ativo = configuracoes.semestre_ativo
            
            # Filtre as cadeiras pelo semestre ativo
            kwargs["queryset"] = Cadeira.objects.filter(semestre=semestre_ativo)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ConfiguracoesAdmin(admin.ModelAdmin):
    list_display = ('semestre_ativo','periodo_inscricao_aberto')
    list_editable = ('periodo_inscricao_aberto',)  # Apenas 'periodo_inscricao_aberto' é editável
    list_display_links = ('semestre_ativo',)  # Defina 'semestre_ativo' como campo de ligação
    

class CadeiraConcluidaAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'curso', 'cadeiras_list')

   

# Aqui você pode adicionar mais configurações personalizadas, se necessário.


admin.site.register(Estudante, EstudanteAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Cadeira, CadeiraAdmin)
admin.site.register(Inscricao, InscricaoAdmin)

admin.site.register(Configuracoes, ConfiguracoesAdmin)
